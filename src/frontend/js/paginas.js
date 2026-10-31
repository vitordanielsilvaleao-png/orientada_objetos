/**
 * Páginas do sistema. Cada tela é uma classe; as telas de listagem herdam de PaginaLista,
 * que cuida de busca, filtros, tabela, estados de carregamento, vazio e erro.
 */

class Pagina {
  constructor(app) {
    this.app = app;
    this.api = app.api;
    this.refs = app.refs;
    this.controle = new AbortController();
  }

  /** Remove os eventos desta tela. Chamado pelo App antes de abrir outra tela. */
  destruir() {
    this.controle.abort();
  }

  cabecalho({ titulo, descricao, acao }) {
    return `
      <header class="cabecalho">
        <div>
          <h1>${esc(titulo)}</h1>
          <span class="ornamento" aria-hidden="true"></span>
          ${descricao ? `<p>${esc(descricao)}</p>` : ''}
        </div>
        ${acao ? `<button class="botao botao-primario" data-acao="novo">${icone('mais')}<span>${esc(acao)}</span></button>` : ''}
      </header>`;
  }

  /** Executa uma operação, avisa o resultado e recarrega a tela. */
  async executar(operacao, mensagemSucesso) {
    try {
      await operacao();
      Toast.mostrar(mensagemSucesso);
      this.refs.invalidar();
      await this.carregar?.();
    } catch (err) {
      Toast.mostrar(err.message, 'erro');
    }
  }

  /** Cria a função de envio de formulário usada pelos modais. */
  envio(operacao, mensagemSucesso) {
    return async (dados) => {
      await operacao(dados);
      Toast.mostrar(mensagemSucesso);
      this.refs.invalidar();
      await this.carregar?.();
    };
  }

  opcoes(chave, { somenteAtivos = false } = {}) {
    return this.refs.lista(chave)
      .filter((i) => !somenteAtivos || estaAtivo(i))
      .map((i) => ({ valor: i.id, texto: i.nome ?? i.titulo }))
      .sort((a, b) => String(a.texto).localeCompare(String(b.texto), 'pt-BR'));
  }
}

class PaginaLista extends Pagina {
  constructor(app) {
    super(app);
    this.itens = [];
    this.busca = '';
    this.mostrarInativos = false;
    this.filtroAtual = null;
  }

  // Valores padrão que as subclasses sobrescrevem
  get filtros() { return null; }
  get temInativos() { return false; }
  get textoBusca() { return 'Buscar'; }
  textoDeBusca(item) { return Object.values(item).join(' '); }
  acoes() { return []; }

  get caminho() { return this.filtroAtual?.caminho ?? this.endpoint; }

  async renderizar(alvo, params = {}) {
    this.alvo = alvo;
    const filtros = this.filtros;
    this.filtroAtual = filtros ? (filtros.find((f) => f.id === params.filtro) || filtros[0]) : null;
    const colunas = this.colunas();

    alvo.innerHTML = `
      ${this.cabecalho({ titulo: this.titulo, descricao: this.descricao, acao: this.textoNovo })}
      <section class="painel-tabela">
        <div class="ferramentas">
          ${filtros ? `
            <div class="abas" role="tablist" aria-label="Filtrar">
              ${filtros.map((f) => `<button type="button" role="tab" class="aba" data-filtro="${f.id}" aria-selected="${f === this.filtroAtual}">${esc(f.rotulo)}</button>`).join('')}
            </div>` : ''}
          <label class="busca">
            ${icone('busca')}
            <input type="search" placeholder="${esc(this.textoBusca)}" aria-label="${esc(this.textoBusca)}">
          </label>
          ${this.temInativos ? `
            <label class="alternar">
              <input type="checkbox" data-inativos>
              <span class="alternar-trilho" aria-hidden="true"></span>
              <span>Mostrar inativos</span>
            </label>` : ''}
        </div>
        <div class="tabela-rolagem">
          <table class="tabela">
            <thead><tr>
              ${colunas.map((c) => `<th scope="col" class="${c.classe || ''}">${esc(c.rotulo)}</th>`).join('')}
              <th scope="col" class="col-acoes"><span class="sr">Ações</span></th>
            </tr></thead>
            <tbody></tbody>
          </table>
        </div>
        <p class="contagem" aria-live="polite"></p>
      </section>`;

    this.tbody = alvo.querySelector('tbody');
    this.contagem = alvo.querySelector('.contagem');

    const { signal } = this.controle;
    alvo.querySelector('.busca input').addEventListener('input', (e) => { this.busca = e.target.value; this.desenhar(); }, { signal });
    alvo.querySelector('[data-inativos]')?.addEventListener('change', (e) => { this.mostrarInativos = e.target.checked; this.desenhar(); }, { signal });
    alvo.querySelectorAll('[data-filtro]').forEach((aba) => aba.addEventListener('click', () => {
      this.filtroAtual = filtros.find((f) => f.id === aba.dataset.filtro);
      alvo.querySelectorAll('[data-filtro]').forEach((a) => a.setAttribute('aria-selected', a === aba));
      this.carregar();
    }, { signal }));
    alvo.addEventListener('click', (e) => this.aoClicar(e), { signal });

    await this.carregar();
    if (params.acao === 'novo') this.novo();
  }

  aoClicar(e) {
    const botao = e.target.closest('[data-acao]');
    if (!botao) return;
    const acao = botao.dataset.acao;
    if (acao === 'novo') return this.novo();
    if (acao === 'tentar') return this.carregar();
    const item = this.itens.find((i) => String(i.id) === botao.dataset.id);
    if (item && typeof this[acao] === 'function') this[acao](item);
  }

  async carregar() {
    const total = this.colunas().length + 1;
    this.tbody.innerHTML = `<tr><td colspan="${total}" class="estado"><span class="girando" aria-hidden="true"></span>Carregando…</td></tr>`;
    this.contagem.textContent = '';
    try {
      await this.refs.carregar();
      this.itens = ApiClient.comoLista(await this.api.get(this.caminho));
      this.desenhar();
    } catch (err) {
      this.tbody.innerHTML = `
        <tr><td colspan="${total}" class="estado estado-erro">
          <strong>Não foi possível carregar os dados.</strong>
          <span>${esc(err.message)}</span>
          <button class="botao botao-secundario" data-acao="tentar">Tentar novamente</button>
        </td></tr>`;
    }
  }

  filtrados() {
    const termo = normalizar(this.busca.trim());
    return this.itens.filter((i) =>
      (!this.temInativos || this.mostrarInativos || estaAtivo(i)) &&
      (!termo || normalizar(this.textoDeBusca(i)).includes(termo)));
  }

  desenhar() {
    const colunas = this.colunas();
    const lista = this.filtrados();
    const [singular, pluralTexto] = this.nomes;

    if (!lista.length) {
      const temBusca = this.busca.trim();
      this.tbody.innerHTML = `
        <tr><td colspan="${colunas.length + 1}" class="estado">
          ${LIRA}
          <strong>${temBusca ? `Nenhum resultado para “${esc(this.busca.trim())}”.` : esc(this.textoVazio)}</strong>
          ${temBusca ? '<span>Confira a grafia ou busque por outro termo.</span>'
            : (this.textoNovo && !this.filtroAtual?.semAcaoVazia ? `<button class="botao botao-secundario" data-acao="novo">${icone('mais')}<span>${esc(this.textoNovo)}</span></button>` : '')}
        </td></tr>`;
      this.contagem.textContent = '';
      return;
    }

    this.tbody.innerHTML = lista.map((item) => `
      <tr class="${this.temInativos && !estaAtivo(item) ? 'inativa' : ''}">
        ${colunas.map((c) => `<td class="${c.classe || ''}" data-rotulo="${esc(c.rotulo)}">${c.valor(item)}</td>`).join('')}
        <td class="col-acoes">
          <div class="acoes">
            ${this.acoes(item).map((a) => a.texto
              ? `<button class="botao botao-pequeno ${a.perigo ? 'botao-perigo-suave' : 'botao-secundario'}" data-acao="${a.id}" data-id="${esc(item.id)}">${icone(a.icone)}<span>${esc(a.texto)}</span></button>`
              : `<button class="botao-icone ${a.perigo ? 'perigo' : ''}" data-acao="${a.id}" data-id="${esc(item.id)}" title="${esc(a.rotulo)}" aria-label="${esc(a.rotulo)}">${icone(a.icone)}</button>`).join('')}
          </div>
        </td>
      </tr>`).join('');

    const ocultos = this.itens.length - lista.length;
    this.contagem.textContent = plural(lista.length, singular, pluralTexto) +
      (ocultos && !this.busca.trim() && this.temInativos ? ` (${ocultos} inativo${ocultos === 1 ? '' : 's'} oculto${ocultos === 1 ? '' : 's'})` : '');
  }

  /** Ações padrão de ativar e inativar, usadas por livros, revistas e clientes. */
  acoesAtivacao(item, rotuloEditar) {
    return [
      { id: 'editar', rotulo: rotuloEditar, icone: 'editar' },
      estaAtivo(item)
        ? { id: 'inativar', rotulo: 'Inativar', icone: 'inativar', perigo: true }
        : { id: 'ativar', rotulo: 'Reativar', icone: 'ativar' },
    ];
  }
}

/* ─────────────── Acervo ─────────────── */

class PaginaLivros extends PaginaLista {
  get titulo() { return 'Livros'; }
  get descricao() { return 'Todos os livros do acervo, com autor, editora e categoria.'; }
  get textoNovo() { return 'Cadastrar livro'; }
  get textoVazio() { return 'Nenhum livro cadastrado ainda.'; }
  get textoBusca() { return 'Buscar por título, autor ou ISBN'; }
  get endpoint() { return '/livro'; }
  get nomes() { return ['livro', 'livros']; }
  get temInativos() { return true; }

  textoDeBusca(i) { return [i.titulo, i.isbn, this.refs.ref(i, 'autor', 'autores')].join(' '); }

  colunas() {
    return [
      { rotulo: 'Título', classe: 'col-principal', valor: (i) => `<strong>${esc(i.titulo)}</strong>${i.isbn ? `<small>ISBN ${esc(i.isbn)}</small>` : ''}` },
      { rotulo: 'Autor', valor: (i) => esc(this.refs.ref(i, 'autor', 'autores')) },
      { rotulo: 'Editora', valor: (i) => esc(this.refs.ref(i, 'editora', 'editoras')) },
      { rotulo: 'Categoria', valor: (i) => esc(this.refs.ref(i, 'categoria', 'categorias')) },
      { rotulo: 'Ano', classe: 'col-numero', valor: (i) => esc(i.ano_publi ?? '—') },
      { rotulo: 'Status', valor: (i) => seloStatus(i.status) },
      { rotulo: 'Situação', valor: (i) => seloAtivo(i) },
    ];
  }

  acoes(item) { return this.acoesAtivacao(item, 'Editar livro'); }

  campos(edicao) {
    return [
      { nome: 'titulo', rotulo: 'Título', obrigatorio: !edicao },
      ...(edicao ? [] : [{ nome: 'isbn', rotulo: 'ISBN', obrigatorio: true, largura: 'meia', placeholder: '978-85-…' }]),
      { nome: 'ano_publi', rotulo: 'Ano de publicação', tipo: 'number', obrigatorio: !edicao, largura: 'meia', min: 0, max: new Date().getFullYear() },
      { nome: 'autor_id', rotulo: 'Autor', tipo: 'select', inteiro: true, obrigatorio: !edicao, opcoes: () => this.opcoes('autores'), avisoSemOpcoes: 'Nenhum autor cadastrado. Cadastre um em Autores primeiro.' },
      { nome: 'editora_id', rotulo: 'Editora', tipo: 'select', inteiro: true, obrigatorio: !edicao, largura: 'meia', opcoes: () => this.opcoes('editoras'), avisoSemOpcoes: 'Cadastre uma editora primeiro.' },
      { nome: 'categoria_id', rotulo: 'Categoria', tipo: 'select', inteiro: true, obrigatorio: !edicao, largura: 'meia', opcoes: () => this.opcoes('categorias'), avisoSemOpcoes: 'Cadastre uma categoria primeiro.' },
    ];
  }

  valoresDe(i) {
    return { ...i, autor_id: this.refs.idRef(i, 'autor'), editora_id: this.refs.idRef(i, 'editora'), categoria_id: this.refs.idRef(i, 'categoria') };
  }

  novo() {
    Modal.formulario({
      titulo: 'Cadastrar livro', campos: this.campos(false), textoBotao: 'Cadastrar livro',
      aoEnviar: this.envio((d) => this.api.post('/livro', d), 'Livro cadastrado.'),
    });
  }

  editar(item) {
    Modal.formulario({
      titulo: 'Editar livro', descricao: item.isbn ? `ISBN ${item.isbn}` : '', campos: this.campos(true),
      valores: this.valoresDe(item), textoBotao: 'Salvar alterações',
      aoEnviar: this.envio((d) => this.api.patch(`/livro/${item.id}`, d), 'Alterações salvas.'),
    });
  }

  async inativar(item) {
    const ok = await Modal.confirmar({
      titulo: 'Inativar livro?', perigo: true, textoBotao: 'Inativar livro',
      mensagem: `“${item.titulo}” deixa de ficar disponível para empréstimos. Você pode reativá-lo depois.`,
    });
    if (ok) this.executar(() => this.api.patch(`/livro/${item.id}/inativar`), 'Livro inativado.');
  }

  ativar(item) { this.executar(() => this.api.patch(`/livro/${item.id}/ativar`), 'Livro reativado.'); }
}

class PaginaRevistas extends PaginaLivros {
  get titulo() { return 'Revistas'; }
  get descricao() { return 'Periódicos do acervo, organizados por edição.'; }
  get textoNovo() { return 'Cadastrar revista'; }
  get textoVazio() { return 'Nenhuma revista cadastrada ainda.'; }
  get textoBusca() { return 'Buscar por título ou ISSN'; }
  get endpoint() { return '/revista'; }
  get nomes() { return ['revista', 'revistas']; }

  textoDeBusca(i) { return [i.titulo, i.issn, i.edicao].join(' '); }

  colunas() {
    return [
      { rotulo: 'Título', classe: 'col-principal', valor: (i) => `<strong>${esc(i.titulo)}</strong>${i.edicao != null ? `<small>Edição ${esc(i.edicao)}</small>` : ''}` },
      { rotulo: 'ISSN', valor: (i) => esc(i.issn ?? '—') },
      { rotulo: 'Editora', valor: (i) => esc(this.refs.ref(i, 'editora', 'editoras')) },
      { rotulo: 'Categoria', valor: (i) => esc(this.refs.ref(i, 'categoria', 'categorias')) },
      { rotulo: 'Ano', classe: 'col-numero', valor: (i) => esc(i.ano_publi ?? '—') },
      { rotulo: 'Status', valor: (i) => seloStatus(i.status) },
      { rotulo: 'Situação', valor: (i) => seloAtivo(i) },
    ];
  }

  acoes(item) { return this.acoesAtivacao(item, 'Editar revista'); }

  campos(edicao) {
    const o = !edicao;
    return [
      { nome: 'titulo', rotulo: 'Título', obrigatorio: o },
      { nome: 'edicao', rotulo: 'Edição', tipo: 'number', obrigatorio: o, largura: 'meia', min: 1 },
      ...(edicao ? [] : [{ nome: 'issn', rotulo: 'ISSN', obrigatorio: true, largura: 'meia', placeholder: '0000-0000' }]),
      { nome: 'ano_publi', rotulo: 'Ano de publicação', tipo: 'number', obrigatorio: o, largura: 'meia', min: 0, max: new Date().getFullYear() },
      { nome: 'editora_id', rotulo: 'Editora', tipo: 'select', inteiro: true, obrigatorio: o, largura: 'meia', opcoes: () => this.opcoes('editoras'), avisoSemOpcoes: 'Cadastre uma editora primeiro.' },
      { nome: 'categoria_id', rotulo: 'Categoria', tipo: 'select', inteiro: true, obrigatorio: o, opcoes: () => this.opcoes('categorias'), avisoSemOpcoes: 'Cadastre uma categoria primeiro.' },
    ];
  }

  novo() {
    Modal.formulario({
      titulo: 'Cadastrar revista', campos: this.campos(false), textoBotao: 'Cadastrar revista',
      aoEnviar: this.envio((d) => this.api.post('/revista', d), 'Revista cadastrada.'),
    });
  }

  editar(item) {
    Modal.formulario({
      titulo: 'Editar revista', campos: this.campos(true), valores: this.valoresDe(item), textoBotao: 'Salvar alterações',
      aoEnviar: this.envio((d) => this.api.patch(`/revista/${item.id}`, d), 'Alterações salvas.'),
    });
  }

  async inativar(item) {
    const ok = await Modal.confirmar({
      titulo: 'Inativar revista?', perigo: true, textoBotao: 'Inativar revista',
      mensagem: `“${item.titulo}” deixa de ficar disponível para empréstimos. Você pode reativá-la depois.`,
    });
    if (ok) this.executar(() => this.api.patch(`/revista/${item.id}/inativar`), 'Revista inativada.');
  }

  ativar(item) { this.executar(() => this.api.patch(`/revista/${item.id}/ativar`), 'Revista reativada.'); }
}

/* ─────────────── Circulação ─────────────── */

function emprestimoDevolvido(e) {
  return Boolean(e.data_devolucao) || /devolv|finaliz|conclu/.test(normalizar(e.status));
}

function reservaAberta(r) {
  return estaAtivo(r) && !/atend|expir|cancel|conclu/.test(normalizar(r.status));
}

class PaginaEmprestimos extends PaginaLista {
  get titulo() { return 'Empréstimos'; }
  get descricao() { return 'Saídas e devoluções de livros e revistas.'; }
  get textoNovo() { return 'Registrar empréstimo'; }
  get textoBusca() { return 'Buscar por material ou cliente'; }
  get endpoint() { return '/emprestimo'; }
  get nomes() { return ['empréstimo', 'empréstimos']; }
  get filtros() {
    return [
      { id: 'abertos', rotulo: 'Em aberto', caminho: '/emprestimo/abertos', vazio: 'Nenhum empréstimo em aberto.' },
      { id: 'atrasados', rotulo: 'Atrasados', caminho: '/emprestimo/atrasados', vazio: 'Nenhum empréstimo atrasado.', semAcaoVazia: true },
      { id: 'todos', rotulo: 'Todos', caminho: '/emprestimo', vazio: 'Nenhum empréstimo registrado ainda.' },
    ];
  }
  get textoVazio() { return this.filtroAtual?.vazio; }

  textoDeBusca(e) { return [this.refs.tituloMaterial(e.material_id), this.refs.nome('clientes', e.cliente_id), e.id].join(' '); }

  colunas() {
    return [
      { rotulo: 'Nº', classe: 'col-numero col-id', valor: (e) => esc(e.id) },
      { rotulo: 'Material', classe: 'col-principal', valor: (e) => `<strong>${esc(this.refs.tituloMaterial(e.material_id))}</strong><small>${esc(this.refs.tipoMaterial(e.material_id))}</small>` },
      { rotulo: 'ID do material', classe: 'col-numero', valor: (e) => esc(e.material_id ?? '—') },
      { rotulo: 'Cliente', valor: (e) => esc(this.refs.nome('clientes', e.cliente_id)) },
      { rotulo: 'Emprestado em', valor: (e) => formatarData(e.data_emprestimo) },
      { rotulo: 'Devolvido em', valor: (e) => formatarData(e.data_devolucao) },
      { rotulo: 'Situação', valor: (e) => seloStatus(e.status || (emprestimoDevolvido(e) ? 'devolvido' : 'aberto')) },
    ];
  }

  acoes(e) {
    return emprestimoDevolvido(e) ? [] : [{ id: 'devolver', texto: 'Registrar devolução', icone: 'devolver' }];
  }

  materiaisDisponiveis() {
    const ocupados = new Set(this.app.emprestimosAbertos.map((e) => String(e.material_id)));
    const formatar = (lista, tipo) => lista
      .filter((m) => estaAtivo(m) && !ocupados.has(String(m.id)))
      .map((m) => ({ valor: m.id, texto: `${m.titulo} (${tipo}${m.edicao != null ? `, ed. ${m.edicao}` : ''})` }));
    return [...formatar(this.refs.lista('livros'), 'livro'), ...formatar(this.refs.lista('revistas'), 'revista')]
      .sort((a, b) => a.texto.localeCompare(b.texto, 'pt-BR'));
  }

  async novo() {
    await this.app.carregarEmprestimosAbertos();
    Modal.formulario({
      titulo: 'Registrar empréstimo', descricao: 'Só aparecem materiais ativos que não estão emprestados.',
      textoBotao: 'Registrar empréstimo',
      campos: [
        { nome: 'material_id', rotulo: 'Livro ou revista', tipo: 'select', inteiro: true, obrigatorio: true, opcoes: () => this.materiaisDisponiveis(), avisoSemOpcoes: 'Nenhum material disponível no momento.' },
        { nome: 'cliente_id', rotulo: 'Cliente', tipo: 'select', inteiro: true, obrigatorio: true, opcoes: () => this.opcoes('clientes', { somenteAtivos: true }), avisoSemOpcoes: 'Cadastre um cliente primeiro.' },
      ],
      aoEnviar: this.envio((d) => this.api.post('/emprestimo', d), 'Empréstimo registrado.'),
    });
  }

  async devolver(e) {
    const ok = await Modal.confirmar({
      titulo: 'Registrar devolução?', textoBotao: 'Registrar devolução',
      mensagem: `“${this.refs.tituloMaterial(e.material_id)}”, emprestado a ${this.refs.nome('clientes', e.cliente_id)} em ${formatarData(e.data_emprestimo)}.`,
    });
    if (ok) this.executar(() => this.api.patch(`/emprestimo/${e.id}/devolver`), 'Devolução registrada.');
  }
}

class PaginaReservas extends PaginaLista {
  get titulo() { return 'Reservas'; }
  get descricao() { return 'Pedidos de clientes que aguardam um título ficar disponível.'; }
  get textoNovo() { return 'Fazer reserva'; }
  get textoBusca() { return 'Buscar por título ou cliente'; }
  get endpoint() { return '/reserva'; }
  get nomes() { return ['reserva', 'reservas']; }
  get filtros() {
    return [
      { id: 'abertas', rotulo: 'Abertas', caminho: '/reserva/abertas', vazio: 'Nenhuma reserva aguardando atendimento.' },
      { id: 'expiradas', rotulo: 'Expiradas', caminho: '/reserva/expiradas', vazio: 'Nenhuma reserva expirada.', semAcaoVazia: true },
      { id: 'todas', rotulo: 'Todas', caminho: '/reserva', vazio: 'Nenhuma reserva registrada ainda.' },
    ];
  }
  get textoVazio() { return this.filtroAtual?.vazio; }

  tituloDe(r) { return r.titulo ?? this.refs.tituloMaterial(r.material_id); }

  /** Usa o material_id da reserva; se a API não enviar, procura o material pelo título. */
  materialIdDe(r) {
    if (r.material_id !== null && r.material_id !== undefined) return r.material_id;
    const titulo = normalizar(r.titulo);
    const material = [...this.refs.lista('livros'), ...this.refs.lista('revistas')].find((m) => normalizar(m.titulo) === titulo);
    return material ? material.id : '—';
  }
  textoDeBusca(r) { return [this.tituloDe(r), this.refs.nome('clientes', r.cliente_id)].join(' '); }

  colunas() {
    return [
      { rotulo: 'Nº', classe: 'col-numero col-id', valor: (r) => esc(r.id) },
      { rotulo: 'Título', classe: 'col-principal', valor: (r) => `<strong>${esc(this.tituloDe(r))}</strong>` },
      { rotulo: 'ID do material', classe: 'col-numero', valor: (r) => esc(this.materialIdDe(r)) },
      { rotulo: 'Cliente', valor: (r) => esc(this.refs.nome('clientes', r.cliente_id)) },
      { rotulo: 'Reservada em', valor: (r) => formatarData(r.data) },
      { rotulo: 'Situação', valor: (r) => seloStatus(r.status || (estaAtivo(r) ? 'aberta' : 'cancelada')) },
    ];
  }

  acoes(r) {
    if (!reservaAberta(r)) return [];
    return [
      { id: 'atender', texto: 'Atender', icone: 'check' },
      { id: 'cancelar', rotulo: 'Cancelar reserva', icone: 'x', perigo: true },
    ];
  }

  novo() {
    const titulos = [...this.refs.lista('livros'), ...this.refs.lista('revistas')].filter(estaAtivo).map((m) => m.titulo);
    Modal.formulario({
      titulo: 'Fazer reserva', textoBotao: 'Fazer reserva',
      campos: [
        { nome: 'titulo', rotulo: 'Título', obrigatorio: true, placeholder: 'Comece a digitar para ver sugestões', sugestoes: () => [...new Set(titulos)] },
        { nome: 'cliente_id', rotulo: 'Cliente', tipo: 'select', inteiro: true, obrigatorio: true, opcoes: () => this.opcoes('clientes', { somenteAtivos: true }), avisoSemOpcoes: 'Cadastre um cliente primeiro.' },
      ],
      aoEnviar: this.envio((d) => this.api.post('/reserva', d), 'Reserva feita.'),
    });
  }

  async atender(r) {
    const ok = await Modal.confirmar({
      titulo: 'Atender reserva?', textoBotao: 'Atender reserva',
      mensagem: `“${this.tituloDe(r)}” para ${this.refs.nome('clientes', r.cliente_id)}.`,
    });
    if (ok) this.executar(() => this.api.patch(`/reserva/${r.id}`), 'Reserva atendida.');
  }

  async cancelar(r) {
    const ok = await Modal.confirmar({
      titulo: 'Cancelar reserva?', perigo: true, textoBotao: 'Cancelar reserva', textoVoltar: 'Manter reserva',
      mensagem: `A reserva de “${this.tituloDe(r)}” para ${this.refs.nome('clientes', r.cliente_id)} será encerrada.`,
    });
    if (ok) this.executar(() => this.api.patch(`/reserva/${r.id}/cancelar`), 'Reserva cancelada.');
  }
}

/* ─────────────── Leitores ─────────────── */

class PaginaClientes extends PaginaLista {
  get titulo() { return 'Clientes'; }
  get descricao() { return 'Leitores cadastrados que podem pegar livros e revistas emprestados.'; }
  get textoNovo() { return 'Cadastrar cliente'; }
  get textoVazio() { return 'Nenhum cliente cadastrado ainda.'; }
  get textoBusca() { return 'Buscar por nome, CPF, telefone ou bairro'; }
  get endpoint() { return '/cliente'; }
  get nomes() { return ['cliente', 'clientes']; }
  get temInativos() { return true; }

  textoDeBusca(c) { return [c.nome, c.cpf, c.telefone, c.bairro, c.rua].join(' '); }

  endereco(c) {
    const linha1 = [c.rua, c.numero].filter((v) => v !== null && v !== undefined && v !== '').join(', ');
    const linha2 = [c.complemento, c.bairro].filter(Boolean).join(', ');
    return `${esc(linha1 || '—')}${linha2 ? `<small>${esc(linha2)}</small>` : ''}`;
  }

  colunas() {
    return [
      { rotulo: 'Nome', classe: 'col-principal', valor: (c) => `<strong>${esc(c.nome)}</strong>${c.cpf ? `<small>CPF ${esc(c.cpf)}</small>` : ''}` },
      { rotulo: 'Telefone', valor: (c) => esc(c.telefone || '—') },
      { rotulo: 'Endereço', classe: 'col-quebra', valor: (c) => this.endereco(c) },
      { rotulo: 'Situação', valor: (c) => seloAtivo(c) },
    ];
  }

  acoes(c) { return this.acoesAtivacao(c, 'Editar cliente'); }

  campos(edicao) {
    const o = !edicao;
    return [
      { nome: 'nome', rotulo: 'Nome completo', obrigatorio: o },
      ...(edicao ? [] : [{ nome: 'cpf', rotulo: 'CPF', obrigatorio: true, placeholder: '000.000.000-00' }]),
      { nome: 'telefone', rotulo: 'Telefone', tipo: 'tel', obrigatorio: o, placeholder: '(00) 00000-0000' },
      { nome: 'rua', rotulo: 'Rua', obrigatorio: o },
      { nome: 'numero', rotulo: 'Número', tipo: 'number', obrigatorio: o, largura: 'meia', min: 0 },
      { nome: 'complemento', rotulo: 'Complemento', largura: 'meia', vazioComo: edicao ? undefined : '' },
      { nome: 'bairro', rotulo: 'Bairro', obrigatorio: o },
    ];
  }

  novo() {
    Modal.formulario({
      titulo: 'Cadastrar cliente', campos: this.campos(false), textoBotao: 'Cadastrar cliente',
      aoEnviar: this.envio((d) => this.api.post('/cliente', d), 'Cliente cadastrado.'),
    });
  }

  editar(c) {
    Modal.formulario({
      titulo: 'Editar cliente', campos: this.campos(true), valores: c, textoBotao: 'Salvar alterações',
      aoEnviar: this.envio((d) => this.api.patch(`/cliente/${c.id}`, d), 'Alterações salvas.'),
    });
  }

  async inativar(c) {
    const ok = await Modal.confirmar({
      titulo: 'Inativar cliente?', perigo: true, textoBotao: 'Inativar cliente',
      mensagem: `${c.nome} não poderá fazer novos empréstimos nem reservas. Você pode reativar o cadastro depois.`,
    });
    if (ok) this.executar(() => this.api.patch(`/cliente/${c.id}/inativar`), 'Cliente inativado.');
  }

  ativar(c) { this.executar(() => this.api.patch(`/cliente/${c.id}/ativar`), 'Cliente reativado.'); }
}

/* ─────────────── Catálogo (autores, editoras, categorias) ─────────────── */

class PaginaCatalogo extends PaginaLista {
  get textoBusca() { return 'Buscar por nome'; }
  textoDeBusca(i) { return i.nome; }

  colunas() {
    return [
      { rotulo: 'Nome', classe: 'col-principal', valor: (i) => `<strong>${esc(i.nome)}</strong>` },
      { rotulo: 'Títulos no acervo', classe: 'col-numero', valor: (i) => esc(this.contarTitulos(i.id)) },
    ];
  }

  contarTitulos(id) {
    const campo = this.campoReferencia;
    return [...this.refs.lista('livros'), ...this.refs.lista('revistas')]
      .filter((m) => String(this.refs.idRef(m, campo)) === String(id)).length;
  }

  acoes() { return [{ id: 'editar', rotulo: `Renomear ${this.nomes[0]}`, icone: 'editar' }]; }

  campoNome() { return [{ nome: 'nome', rotulo: 'Nome', obrigatorio: true }]; }

  novo() {
    Modal.formulario({
      titulo: this.textoNovo, campos: this.campoNome(), textoBotao: this.textoNovo,
      aoEnviar: this.envio((d) => this.api.post(this.caminhoCadastro, d), this.mensagemCadastro),
    });
  }

  editar(item) {
    Modal.formulario({
      titulo: `Renomear ${this.nomes[0]}`, campos: this.campoNome(), valores: item, textoBotao: 'Salvar nome',
      aoEnviar: this.envio((d) => this.renomear(item, d.nome), 'Nome salvo.'),
    });
  }
}

class PaginaAutores extends PaginaCatalogo {
  get titulo() { return 'Autores'; }
  get descricao() { return 'Quem escreveu as obras do acervo.'; }
  get textoNovo() { return 'Cadastrar autor'; }
  get textoVazio() { return 'Nenhum autor cadastrado ainda.'; }
  get endpoint() { return '/autor'; }
  get caminhoCadastro() { return '/autor'; }
  get mensagemCadastro() { return 'Autor cadastrado.'; }
  get nomes() { return ['autor', 'autores']; }
  get campoReferencia() { return 'autor'; }
  renomear(item, nome) { return this.api.patch(`/autor/${item.id}`, { nome }); }
}

class PaginaEditoras extends PaginaCatalogo {
  get titulo() { return 'Editoras'; }
  get descricao() { return 'Casas editoriais responsáveis pelos livros e revistas.'; }
  get textoNovo() { return 'Cadastrar editora'; }
  get textoVazio() { return 'Nenhuma editora cadastrada ainda.'; }
  get endpoint() { return '/editora'; }
  get caminhoCadastro() { return '/editora'; }
  get mensagemCadastro() { return 'Editora cadastrada.'; }
  get nomes() { return ['editora', 'editoras']; }
  get campoReferencia() { return 'editora'; }
  renomear(item, nome) { return this.api.patch(`/editora/${item.id}`, { nome }); }
}

class PaginaCategorias extends PaginaCatalogo {
  get titulo() { return 'Categorias'; }
  get descricao() { return 'Gêneros e assuntos usados para organizar o acervo.'; }
  get textoNovo() { return 'Cadastrar categoria'; }
  get textoVazio() { return 'Nenhuma categoria cadastrada ainda.'; }
  get endpoint() { return '/categoria'; }
  get caminhoCadastro() { return '/categoria'; }
  get mensagemCadastro() { return 'Categoria cadastrada.'; }
  get nomes() { return ['categoria', 'categorias']; }
  get campoReferencia() { return 'categoria'; }
  renomear(item, nome) { return this.api.patch(`/categoria/${item.id}`, { nome }); }
}

/* ─────────────── Painel ─────────────── */

class PaginaPainel extends Pagina {
  async renderizar(alvo) {
    const agora = new Date();
    const hora = agora.getHours() + agora.getMinutes() / 60;
    const dia = hora >= 6 && hora < 18;
    const saudacao = hora < 5 ? 'Boa noite' : hora < 12 ? 'Bom dia' : hora < 18 ? 'Boa tarde' : 'Boa noite';
    const dataTexto = capitalizar(agora.toLocaleDateString('pt-BR', { weekday: 'long', day: 'numeric', month: 'long' }));

    alvo.innerHTML = `
      <section class="ceu ${dia ? 'ceu-dia' : 'ceu-noite'}">
        <svg class="ceu-arco" viewBox="0 0 600 220" preserveAspectRatio="xMidYMax meet" aria-hidden="true">
          <path d="M40 210 A260 170 0 0 1 560 210" class="arco"/>
          <g class="astro">${dia
            ? `<circle r="34" class="sol-halo"/><circle r="20" class="sol"/>${Array.from({ length: 12 }, (_, i) => {
                const a = (i * Math.PI) / 6;
                return `<line x1="${(Math.cos(a) * 26).toFixed(1)}" y1="${(Math.sin(a) * 26).toFixed(1)}" x2="${(Math.cos(a) * 33).toFixed(1)}" y2="${(Math.sin(a) * 33).toFixed(1)}" class="raio"/>`;
              }).join('')}`
            : '<circle r="18" class="lua"/><circle r="16" cx="8" cy="-5" class="lua-sombra"/>'}
          </g>
          ${dia ? '' : this.estrelas()}
        </svg>
        <div class="ceu-texto">
          <p class="ceu-data">${esc(dataTexto)}</p>
          <h1>${saudacao}.</h1>
          <p class="ceu-resumo" id="resumo">Consultando o acervo…</p>
          <div class="ceu-acoes">
            <a class="botao botao-primario" href="#/emprestimos?acao=novo">${icone('emprestimo')}<span>Registrar empréstimo</span></a>
            <a class="botao botao-claro" href="#/reservas?acao=novo">${icone('reserva')}<span>Fazer reserva</span></a>
          </div>
        </div>
        <div class="meandro meandro-ceu" aria-hidden="true"></div>
      </section>

      <section class="numeros" id="numeros" aria-label="Resumo do acervo"></section>

      <div class="colunas-painel">
        <section class="lista-painel">
          <header><h2>Empréstimos atrasados</h2><a href="#/emprestimos?filtro=atrasados">Ver todos</a></header>
          <ul id="listaAtrasados"><li class="estado"><span class="girando"></span>Carregando…</li></ul>
        </section>
        <section class="lista-painel">
          <header><h2>Reservas aguardando</h2><a href="#/reservas">Ver todas</a></header>
          <ul id="listaReservas"><li class="estado"><span class="girando"></span>Carregando…</li></ul>
        </section>
      </div>`;

    this.posicionarAstro(alvo.querySelector('.astro'), dia ? (hora - 6) / 12 : ((hora - 18 + 24) % 24) / 12);
    await this.carregarDados(alvo);
  }

  /** Pequenas estrelas espalhadas pelo céu noturno. */
  estrelas() {
    const pontos = [[90, 60], [150, 120], [220, 40], [300, 95], [380, 30], [430, 140], [500, 70], [560, 120], [260, 160], [120, 175], [470, 185], [340, 180]];
    return `<g class="estrelas">${pontos.map(([x, y], i) => `<circle cx="${x}" cy="${y}" r="${i % 3 ? 1.2 : 1.9}"/>`).join('')}</g>`;
  }

  /** Move o sol (ou a lua) pelo arco do céu conforme a hora. t vai de 0 (nascente) a 1 (poente). */
  posicionarAstro(astro, t) {
    const ponto = (p) => {
      const ang = Math.PI * (1 - p);
      return [300 + 260 * Math.cos(ang), 210 - 170 * Math.sin(ang)];
    };
    const [x0, y0] = ponto(0.02);
    const [x, y] = ponto(Math.min(Math.max(t, 0.04), 0.96));
    astro.style.transform = `translate(${x0}px, ${y0}px)`;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      astro.style.transform = `translate(${x}px, ${y}px)`;
      return;
    }
    requestAnimationFrame(() => requestAnimationFrame(() => {
      astro.classList.add('subindo');
      astro.style.transform = `translate(${x}px, ${y}px)`;
    }));
  }

  async carregarDados(alvo) {
    const [refs, abertos, atrasados, reservas] = await Promise.allSettled([
      this.refs.carregar(),
      this.api.get('/emprestimo/abertos'),
      this.api.get('/emprestimo/atrasados'),
      this.api.get('/reserva/abertas'),
    ]);
    const valor = (r) => (r.status === 'fulfilled' ? ApiClient.comoLista(r.value) : null);
    const listaAbertos = valor(abertos);
    const listaAtrasados = valor(atrasados);
    const listaReservas = valor(reservas)?.filter(reservaAberta) ?? null;
    const ativos = (chave) => (refs.status === 'fulfilled' && !this.refs.falhou(chave) ? this.refs.lista(chave).filter(estaAtivo).length : null);

    // Resumo em frase
    const resumo = alvo.querySelector('#resumo');
    if (!listaAbertos && !listaAtrasados) {
      resumo.textContent = 'Não foi possível consultar a API. Verifique a conexão e recarregue a página.';
    } else {
      const partes = [];
      const nAtrasados = listaAtrasados?.length ?? 0;
      const nAbertos = listaAbertos?.length ?? 0;
      const nReservas = listaReservas?.length ?? 0;
      if (nAtrasados) partes.push(`${plural(nAtrasados, 'empréstimo está atrasado', 'empréstimos estão atrasados')}`);
      partes.push(nAbertos ? `${plural(nAbertos, 'empréstimo segue', 'empréstimos seguem')} em aberto` : 'não há empréstimos em aberto');
      if (nReservas) partes.push(`${plural(nReservas, 'reserva aguarda', 'reservas aguardam')} atendimento`);
      const frase = partes.length > 1 ? `${partes.slice(0, -1).join(', ')} e ${partes[partes.length - 1]}` : partes[0];
      resumo.textContent = `${capitalizar(frase)}.${nAtrasados ? '' : ' Nenhum atraso por aqui.'}`;
    }

    // Números
    const numeros = [
      { rotulo: 'Livros ativos', valor: ativos('livros'), rota: 'livros' },
      { rotulo: 'Revistas ativas', valor: ativos('revistas'), rota: 'revistas' },
      { rotulo: 'Clientes ativos', valor: ativos('clientes'), rota: 'clientes' },
      { rotulo: 'Empréstimos em aberto', valor: listaAbertos?.length, rota: 'emprestimos?filtro=abertos' },
      { rotulo: 'Atrasados', valor: listaAtrasados?.length, rota: 'emprestimos?filtro=atrasados', alerta: true },
      { rotulo: 'Reservas abertas', valor: listaReservas?.length, rota: 'reservas' },
    ];
    alvo.querySelector('#numeros').innerHTML = numeros.map((n) => `
      <a class="numero ${n.alerta && n.valor ? 'numero-alerta' : ''}" href="#/${n.rota}">
        <span class="numero-valor">${n.valor ?? '—'}</span>
        <span class="numero-rotulo">${esc(n.rotulo)}</span>
      </a>`).join('');

    // Listas
    const ul = alvo.querySelector('#listaAtrasados');
    if (!listaAtrasados) ul.innerHTML = '<li class="estado">Não foi possível carregar os atrasos.</li>';
    else if (!listaAtrasados.length) ul.innerHTML = '<li class="estado">Nenhum empréstimo atrasado. Tudo devolvido no prazo.</li>';
    else {
      ul.innerHTML = listaAtrasados.slice(0, 6).map((e) => `
        <li>
          <div><strong>${esc(this.refs.tituloMaterial(e.material_id))}</strong><small>${esc(this.refs.nome('clientes', e.cliente_id))}</small></div>
          <span class="lista-meta">desde ${formatarData(e.data_emprestimo)}</span>
        </li>`).join('');
    }

    const ur = alvo.querySelector('#listaReservas');
    if (!listaReservas) ur.innerHTML = '<li class="estado">Não foi possível carregar as reservas.</li>';
    else if (!listaReservas.length) ur.innerHTML = '<li class="estado">Nenhuma reserva aguardando atendimento.</li>';
    else {
      ur.innerHTML = listaReservas.slice(0, 6).map((r) => `
        <li>
          <div><strong>${esc(r.titulo ?? this.refs.tituloMaterial(r.material_id))}</strong><small>${esc(this.refs.nome('clientes', r.cliente_id))}</small></div>
          <span class="lista-meta">desde ${formatarData(r.data)}</span>
        </li>`).join('');
    }
  }
}

/* ─────────────── Relatórios ─────────────── */

const UM_DIA = 24 * 60 * 60 * 1000;

/** Data limite de devolução, somando o prazo à data do empréstimo. */
function prazoDevolucao(e) {
  return new Date(new Date(e.data_emprestimo).getTime() + CONFIG.PRAZO_EMPRESTIMO_DIAS * UM_DIA);
}

/** Dias inteiros de uma data até agora (negativo se a data ainda não chegou). */
function diasDesde(data) {
  return Math.floor((Date.now() - new Date(data).getTime()) / UM_DIA);
}

/**
 * Gráfico de barras horizontais simples.
 * itens: [{ rotulo, detalhe, valor, dica }]; com ranking, mostra a posição e a coroa de louros no 1º lugar.
 */
function graficoBarras(itens, { ranking = false } = {}) {
  const maximo = Math.max(...itens.map((i) => i.valor), 1);
  return `
    <ol class="grafico ${ranking ? 'grafico-ranking' : ''}">
      ${itens.map((i, pos) => `
        <li class="grafico-item" title="${esc(i.dica ?? `${i.rotulo}: ${i.valor}`)}">
          ${ranking ? `<span class="grafico-pos">${pos === 0 ? icone('louro') : pos + 1}</span>` : ''}
          <div class="grafico-texto">
            <span class="grafico-rotulo">${esc(i.rotulo)}${i.detalhe ? `<small>${esc(i.detalhe)}</small>` : ''}</span>
            <span class="grafico-valor">${esc(i.valor)}</span>
          </div>
          <div class="grafico-trilho"><span class="grafico-barra" style="width: ${((i.valor / maximo) * 100).toFixed(1)}%"></span></div>
        </li>`).join('')}
    </ol>`;
}

class PaginaRelatorios extends Pagina {
  static LIMITE_RANKING = 10;
  static LIMITE_CATEGORIAS = 8;

  async renderizar(alvo) {
    alvo.innerHTML = `
      <header class="cabecalho">
        <div>
          <h1>Relatórios</h1>
          <span class="ornamento" aria-hidden="true"></span>
          <p>O que o oráculo vê no acervo e na circulação, com os dados atuais da API.</p>
        </div>
        <button class="botao botao-secundario" data-acao="imprimir">${icone('imprimir')}<span>Imprimir</span></button>
      </header>

      <section class="numeros numeros-quatro" id="relNumeros" aria-label="Situação do acervo">
        <p class="estado"><span class="girando"></span>Carregando…</p>
      </section>

      ${this.secao('relRanking', 'Materiais mais emprestados', 'Todos os empréstimos já registrados, inclusive os devolvidos.')}
      ${this.secao('relAbertos', 'Empréstimos em aberto', `Materiais fora da biblioteca. O prazo de devolução é de ${CONFIG.PRAZO_EMPRESTIMO_DIAS} dias.`)}
      ${this.secao('relAtrasados', 'Devoluções atrasadas', 'Empréstimos marcados como atrasados, do maior atraso para o menor.')}

      <div class="colunas-painel">
        ${this.secao('relTipo', 'Acervo por tipo', 'Livros e revistas cadastrados.')}
        ${this.secao('relCategoria', 'Acervo por categoria', 'Quantidade de títulos em cada categoria.')}
      </div>`;

    alvo.addEventListener('click', (e) => {
      if (e.target.closest('[data-acao="imprimir"]')) window.print();
    }, { signal: this.controle.signal });

    await this.carregarDados(alvo);
  }

  secao(id, titulo, descricao) {
    return `
      <section class="relatorio" id="${id}">
        <header><h2>${esc(titulo)}</h2><p>${esc(descricao)}</p></header>
        <div class="relatorio-corpo"><p class="estado"><span class="girando"></span>Carregando…</p></div>
      </section>`;
  }

  preencher(alvo, id, html) {
    alvo.querySelector(`#${id} .relatorio-corpo`).innerHTML = html;
  }

  vazio(texto) {
    return `<div class="estado">${LIRA}<strong>${esc(texto)}</strong></div>`;
  }

  falha(texto) {
    return `<div class="estado estado-erro"><strong>${esc(texto)}</strong><span>Verifique a conexão com a API e recarregue a página.</span></div>`;
  }

  async carregarDados(alvo) {
    const respostas = await Promise.allSettled([
      this.refs.carregar(),
      this.api.get('/material/quantidade/total'),
      this.api.get('/material/quantidade/disponiveis'),
      this.api.get('/material/emprestados'),
      this.api.get('/material/quantidade/tipo'),
      this.api.get('/material/quantidade/categoria'),
      this.api.get('/emprestimo'),
      this.api.get('/emprestimo/abertos'),
      this.api.get('/emprestimo/atrasados'),
    ]);
    const [, total, disponiveis, emprestados, porTipo, porCategoria, todos, abertos, atrasados] =
      respostas.map((r) => (r.status === 'fulfilled' ? r.value : null));
    const lista = (v) => (v ? ApiClient.comoLista(v) : null);

    // Os títulos dos materiais emprestados vêm do MaterialRouter; o catálogo geral cobre o resto
    const emprestadosPorId = new Map((lista(emprestados) || []).map((m) => [String(m.id), m]));
    this.material = (id) => emprestadosPorId.get(String(id)) || this.refs.material(id);

    this.desenharNumeros(alvo, total, disponiveis, lista(emprestados), lista(atrasados));
    this.desenharRanking(alvo, lista(todos));
    this.desenharAbertos(alvo, lista(abertos));
    this.desenharAtrasados(alvo, lista(atrasados));
    this.desenharTipos(alvo, lista(porTipo));
    this.desenharCategorias(alvo, lista(porCategoria));
  }

  titulo(id) { return this.material(id)?.titulo ?? `Material #${id}`; }
  tipo(id) {
    const tipo = this.material(id)?.tipo;
    return tipo ? capitalizar(tipo) : this.refs.tipoMaterial(id);
  }

  desenharNumeros(alvo, total, disponiveis, emprestados, atrasados) {
    const numeros = [
      { rotulo: 'Materiais no acervo', valor: total?.quantidade, rota: 'livros' },
      { rotulo: 'Disponíveis', valor: disponiveis?.quantidade, rota: 'livros' },
      { rotulo: 'Emprestados', valor: emprestados?.length, rota: 'emprestimos?filtro=abertos' },
      { rotulo: 'Devoluções atrasadas', valor: atrasados?.length, rota: 'emprestimos?filtro=atrasados', alerta: true },
    ];
    alvo.querySelector('#relNumeros').innerHTML = numeros.map((n) => `
      <a class="numero ${n.alerta && n.valor ? 'numero-alerta' : ''}" href="#/${n.rota}">
        <span class="numero-valor">${n.valor ?? '—'}</span>
        <span class="numero-rotulo">${esc(n.rotulo)}</span>
      </a>`).join('');
  }

  desenharRanking(alvo, emprestimos) {
    if (!emprestimos) return this.preencher(alvo, 'relRanking', this.falha('Não foi possível carregar os empréstimos.'));
    if (!emprestimos.length) return this.preencher(alvo, 'relRanking', this.vazio('Nenhum empréstimo registrado ainda.'));

    const contagem = new Map();
    for (const e of emprestimos) contagem.set(e.material_id, (contagem.get(e.material_id) || 0) + 1);
    const itens = [...contagem.entries()]
      .map(([id, valor]) => ({
        rotulo: this.titulo(id), detalhe: this.tipo(id), valor,
        dica: `${this.titulo(id)}: ${plural(valor, 'empréstimo', 'empréstimos')}`,
      }))
      .sort((a, b) => b.valor - a.valor || a.rotulo.localeCompare(b.rotulo, 'pt-BR'))
      .slice(0, PaginaRelatorios.LIMITE_RANKING);
    this.preencher(alvo, 'relRanking', graficoBarras(itens, { ranking: true }));
  }

  tabela(colunas, linhas) {
    return `
      <div class="tabela-rolagem">
        <table class="tabela">
          <thead><tr>${colunas.map((c) => `<th scope="col" class="${c.classe || ''}">${esc(c.rotulo)}</th>`).join('')}</tr></thead>
          <tbody>${linhas.map((l) => `<tr>${colunas.map((c) => `<td class="${c.classe || ''}" data-rotulo="${esc(c.rotulo)}">${c.valor(l)}</td>`).join('')}</tr>`).join('')}</tbody>
        </table>
      </div>`;
  }

  colunaMaterial() {
    return { rotulo: 'Material', classe: 'col-principal', valor: (e) => `<strong>${esc(this.titulo(e.material_id))}</strong><small>${esc(this.tipo(e.material_id))}</small>` };
  }

  desenharAbertos(alvo, abertos) {
    if (!abertos) return this.preencher(alvo, 'relAbertos', this.falha('Não foi possível carregar os empréstimos em aberto.'));
    if (!abertos.length) return this.preencher(alvo, 'relAbertos', this.vazio('Nenhum empréstimo em aberto.'));

    const linhas = [...abertos].sort((a, b) => prazoDevolucao(a) - prazoDevolucao(b));
    this.preencher(alvo, 'relAbertos', this.tabela([
      this.colunaMaterial(),
      { rotulo: 'Cliente', valor: (e) => esc(this.refs.nome('clientes', e.cliente_id)) },
      { rotulo: 'Emprestado em', valor: (e) => formatarData(e.data_emprestimo) },
      { rotulo: 'Devolver até', valor: (e) => formatarData(prazoDevolucao(e)) },
      { rotulo: 'Prazo', valor: (e) => {
        const restam = -diasDesde(prazoDevolucao(e));
        if (restam < 0) return selo(`Vencido há ${plural(-restam, 'dia', 'dias')}`, 'granada');
        if (restam === 0) return selo('Vence hoje', 'ouro');
        return selo(`${plural(restam, 'dia restante', 'dias restantes')}`, restam <= 3 ? 'ouro' : 'louro');
      } },
    ], linhas));
  }

  desenharAtrasados(alvo, atrasados) {
    if (!atrasados) return this.preencher(alvo, 'relAtrasados', this.falha('Não foi possível carregar os atrasos.'));
    if (!atrasados.length) return this.preencher(alvo, 'relAtrasados', this.vazio('Nenhuma devolução atrasada. Tudo no prazo.'));

    const linhas = [...atrasados].sort((a, b) => prazoDevolucao(a) - prazoDevolucao(b));
    this.preencher(alvo, 'relAtrasados', this.tabela([
      this.colunaMaterial(),
      { rotulo: 'Cliente', valor: (e) => esc(this.refs.nome('clientes', e.cliente_id)) },
      { rotulo: 'Telefone', valor: (e) => esc(this.refs.porId('clientes', e.cliente_id)?.telefone ?? '—') },
      { rotulo: 'Venceu em', valor: (e) => formatarData(prazoDevolucao(e)) },
      { rotulo: 'Dias de atraso', classe: 'col-numero', valor: (e) => `<span class="atraso">${Math.max(diasDesde(prazoDevolucao(e)), 0)}</span>` },
    ], linhas));
  }

  desenharTipos(alvo, porTipo) {
    if (!porTipo) return this.preencher(alvo, 'relTipo', this.falha('Não foi possível carregar as quantidades por tipo.'));
    if (!porTipo.length) return this.preencher(alvo, 'relTipo', this.vazio('Nenhum material cadastrado ainda.'));

    const itens = porTipo
      .map((t) => ({ rotulo: capitalizar(t.tipo), valor: t.quantidade }))
      .sort((a, b) => b.valor - a.valor);
    this.preencher(alvo, 'relTipo', graficoBarras(itens));
  }

  /** Mostra as maiores categorias e agrupa o restante em "Outras", para a lista não crescer sem limite. */
  desenharCategorias(alvo, porCategoria) {
    if (!porCategoria) return this.preencher(alvo, 'relCategoria', this.falha('Não foi possível carregar as quantidades por categoria.'));
    if (!porCategoria.length) return this.preencher(alvo, 'relCategoria', this.vazio('Nenhum material cadastrado ainda.'));

    const ordenadas = porCategoria
      .map((c) => ({ rotulo: this.refs.nome('categorias', c.categoria_id), valor: c.quantidade }))
      .sort((a, b) => b.valor - a.valor || a.rotulo.localeCompare(b.rotulo, 'pt-BR'));
    const limite = PaginaRelatorios.LIMITE_CATEGORIAS;
    const itens = ordenadas.slice(0, limite);
    const resto = ordenadas.slice(limite);
    if (resto.length) {
      itens.push({ rotulo: 'Outras', detalhe: plural(resto.length, 'categoria', 'categorias'), valor: resto.reduce((s, c) => s + c.valor, 0) });
    }
    this.preencher(alvo, 'relCategoria', graficoBarras(itens));
  }
}
