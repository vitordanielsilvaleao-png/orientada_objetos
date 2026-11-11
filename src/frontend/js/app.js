/**
 * Ponto de entrada: monta o menu, controla a navegação e mantém em cache
 * os dados usados para mostrar nomes no lugar de ids (autores, editoras, etc.).
 */

class Referencias {
  static RECURSOS = {
    autores: '/autor', categorias: '/categoria', editoras: '/editora',
    livros: '/livro', revistas: '/revista', clientes: '/cliente', materiais: '/material',
  };

  constructor(api) {
    this.api = api;
    this.dados = {};
    this.falhas = new Set();
    this.promessa = null;
  }

  carregar() {
    if (!this.promessa) {
      this.falhas.clear();
      this.promessa = Promise.all(Object.entries(Referencias.RECURSOS).map(async ([chave, caminho]) => {
        try {
          this.dados[chave] = ApiClient.comoLista(await this.api.get(caminho));
        } catch {
          this.dados[chave] = this.dados[chave] || [];
          this.falhas.add(chave);
        }
      })).then(() => this.dados);
    }
    return this.promessa;
  }

  invalidar() { this.promessa = null; }
  falhou(chave) { return this.falhas.has(chave); }
  lista(chave) { return this.dados[chave] || []; }
  porId(chave, id) { return this.lista(chave).find((i) => String(i.id) === String(id)); }

  nome(chave, id) {
    if (id === null || id === undefined) return '—';
    const item = this.porId(chave, id);
    return item ? (item.nome ?? item.titulo) : `#${id}`;
  }

  /** Id de uma referência, aceitando tanto { autor_id: 1 } quanto { autor: { id: 1 } }. */
  idRef(item, campo) {
    return item[`${campo}_id`] ?? (item[campo] && typeof item[campo] === 'object' ? item[campo].id : undefined);
  }

  /** Nome de uma referência, aceitando id, objeto aninhado ou texto já resolvido pela API. */
  ref(item, campo, chave) {
    const valor = item[campo];
    if (valor && typeof valor === 'object') return valor.nome ?? valor.titulo ?? '—';
    if (typeof valor === 'string' && valor) return valor;
    return this.nome(chave, item[`${campo}_id`]);
  }

  /** Livros e revistas compartilham o id da tabela material, então o catálogo geral resolve os dois. */
  material(id) { return this.porId('materiais', id) || this.porId('livros', id) || this.porId('revistas', id); }
  tituloMaterial(id) { return this.material(id)?.titulo ?? `Material #${id}`; }
  tipoMaterial(id) {
    const tipo = this.porId('materiais', id)?.tipo;
    if (tipo) return capitalizar(tipo);
    if (this.porId('livros', id)) return 'Livro';
    if (this.porId('revistas', id)) return 'Revista';
    return 'Material';
  }
}

const MENU = [
  { itens: [{ rota: 'painel', rotulo: 'Painel', icone: 'painel' }] },
  { grupo: 'Acervo', itens: [
    { rota: 'livros', rotulo: 'Livros', icone: 'livro' },
    { rota: 'revistas', rotulo: 'Revistas', icone: 'revista' },
  ] },
  { grupo: 'Circulação', itens: [
    { rota: 'emprestimos', rotulo: 'Empréstimos', icone: 'emprestimo' },
    { rota: 'reservas', rotulo: 'Reservas', icone: 'reserva' },
  ] },
  { grupo: 'Oráculo', itens: [{ rota: 'relatorios', rotulo: 'Relatórios', icone: 'relatorio' }] },
  { grupo: 'Leitores', itens: [{ rota: 'clientes', rotulo: 'Clientes', icone: 'cliente' }] },
  { grupo: 'Catálogo', itens: [
    { rota: 'autores', rotulo: 'Autores', icone: 'autor' },
    { rota: 'editoras', rotulo: 'Editoras', icone: 'editora' },
    { rota: 'categorias', rotulo: 'Categorias', icone: 'categoria' },
  ] },
];

class App {
  constructor() {
    this.api = CONFIG.MODO_DEMO ? new ApiDemo() : new ApiClient(CONFIG.API_URL);
    this.refs = new Referencias(this.api);
    this.emprestimosAbertos = [];
    this.rotas = {
      painel: PaginaPainel, livros: PaginaLivros, revistas: PaginaRevistas,
      emprestimos: PaginaEmprestimos, reservas: PaginaReservas, clientes: PaginaClientes,
      autores: PaginaAutores, editoras: PaginaEditoras, categorias: PaginaCategorias,
      relatorios: PaginaRelatorios,
    };
    this.alvo = document.getElementById('pagina');
    this.barra = document.getElementById('barra');
    this.fundo = document.getElementById('fundoMenu');
    this.botaoMenu = document.getElementById('abrirMenu');
  }

  iniciar() {
    this.montarMarca();
    this.montarMenu();
    Modal.iniciar();
    this.botaoMenu.innerHTML = icone('menu');
    this.botaoMenu.addEventListener('click', () => this.alternarMenu(true));
    this.fundo.addEventListener('click', () => this.alternarMenu(false));
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') this.alternarMenu(false); });
    window.addEventListener('hashchange', () => this.navegar());
    this.navegar();
    this.verificarApi();
  }

  montarMarca() {
    const raios = Array.from({ length: 12 }, (_, i) => {
      const a = (i * Math.PI) / 6;
      const p = (r) => [(24 + Math.cos(a) * r).toFixed(2), (24 + Math.sin(a) * r).toFixed(2)];
      const [x1, y1] = p(14);
      const [x2, y2] = p(i % 2 ? 19 : 21);
      return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}"/>`;
    }).join('');
    document.getElementById('marca').innerHTML = `
      <svg class="marca-sol" viewBox="0 0 48 48" aria-hidden="true">
        <circle cx="24" cy="24" r="9"/><g>${raios}</g>
      </svg>
      <span class="marca-texto">
        <span class="marca-nome">Apolo</span>
        <span class="marca-sub">Gestão de biblioteca</span>
      </span>`;
  }

  montarMenu() {
    document.getElementById('menu').innerHTML = MENU.map((secao) => `
      <div class="menu-secao">
        ${secao.grupo ? `<p class="menu-grupo">${esc(secao.grupo)}</p>` : ''}
        ${secao.itens.map((i) => `<a href="#/${i.rota}" class="menu-item" data-rota="${i.rota}">${icone(i.icone)}<span>${esc(i.rotulo)}</span></a>`).join('')}
      </div>`).join('');
  }

  alternarMenu(abrir) {
    this.barra.classList.toggle('aberta', abrir);
    this.fundo.hidden = !abrir;
    this.botaoMenu.setAttribute('aria-expanded', String(abrir));
  }

  async navegar() {
    const [rota, consulta] = window.location.hash.replace(/^#\/?/, '').split('?');
    const nome = this.rotas[rota] ? rota : 'painel';
    const params = Object.fromEntries(new URLSearchParams(consulta || ''));

    document.querySelectorAll('.menu-item').forEach((a) => {
      const atual = a.dataset.rota === nome;
      a.classList.toggle('ativo', atual);
      if (atual) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
    });
    this.alternarMenu(false);

    const item = MENU.flatMap((s) => s.itens).find((i) => i.rota === nome);
    document.title = `${item.rotulo} | Apolo`;

    this.paginaAtual?.destruir();
    this.paginaAtual = new this.rotas[nome](this);
    this.alvo.scrollTop = 0;
    window.scrollTo(0, 0);
    await this.paginaAtual.renderizar(this.alvo, params);
    this.alvo.focus({ preventScroll: true });
  }

  async carregarEmprestimosAbertos() {
    try {
      this.emprestimosAbertos = ApiClient.comoLista(await this.api.get('/emprestimo/abertos'));
    } catch {
      this.emprestimosAbertos = [];
    }
    await this.refs.carregar();
  }

  async verificarApi() {
    const status = document.getElementById('statusApi');
    const texto = status.querySelector('.texto');
    if (CONFIG.MODO_DEMO) {
      status.dataset.estado = 'demo';
      texto.textContent = 'Modo demonstração';
      return;
    }
    try {
      await this.api.get('/categoria');
      status.dataset.estado = 'ok';
      texto.textContent = 'Conectado à API';
    } catch {
      status.dataset.estado = 'erro';
      texto.textContent = 'API indisponível';
    }
  }
}

document.addEventListener('DOMContentLoaded', () => new App().iniciar());
