/**
 * API de demonstração: imita as rotas da API real com dados em memória.
 * Serve para visualizar o front sem o back-end rodando (index.html?demo).
 */
class ApiDemo extends ApiClient {
  constructor() {
    super('demo');
    const dia = 24 * 60 * 60 * 1000;
    const atras = (dias) => new Date(Date.now() - dias * dia).toISOString();

    this.db = {
      autores: [
        { id: 1, nome: 'Machado de Assis' },
        { id: 2, nome: 'Clarice Lispector' },
        { id: 3, nome: 'João Guimarães Rosa' },
        { id: 4, nome: 'Cecília Meireles' },
        { id: 5, nome: 'Homero' },
      ],
      categorias: [
        { id: 1, nome: 'Romance' },
        { id: 2, nome: 'Poesia' },
        { id: 3, nome: 'Clássicos' },
        { id: 4, nome: 'Ciência e cultura' },
      ],
      editoras: [
        { id: 1, nome: 'Companhia das Letras' },
        { id: 2, nome: 'Editora 34' },
        { id: 3, nome: 'Rocco' },
        { id: 4, nome: 'Nova Fronteira' },
      ],
      livros: [
        { id: 1, titulo: 'Dom Casmurro', ano_publi: 1899, isbn: '978-85-359-0277-1', autor_id: 1, editora_id: 1, categoria_id: 1, is_active: true },
        { id: 2, titulo: 'Memórias póstumas de Brás Cubas', ano_publi: 1881, isbn: '978-85-359-1022-6', autor_id: 1, editora_id: 1, categoria_id: 1, is_active: true },
        { id: 3, titulo: 'A hora da estrela', ano_publi: 1977, isbn: '978-85-325-0812-9', autor_id: 2, editora_id: 3, categoria_id: 1, is_active: true },
        { id: 4, titulo: 'Grande sertão: veredas', ano_publi: 1956, isbn: '978-85-209-2325-1', autor_id: 3, editora_id: 4, categoria_id: 1, is_active: true },
        { id: 5, titulo: 'Romanceiro da Inconfidência', ano_publi: 1953, isbn: '978-85-260-1386-8', autor_id: 4, editora_id: 4, categoria_id: 2, is_active: true },
        { id: 6, titulo: 'Odisseia', ano_publi: 2011, isbn: '978-85-7326-479-0', autor_id: 5, editora_id: 2, categoria_id: 3, is_active: false },
      ],
      revistas: [
        { id: 7, titulo: 'Pesquisa FAPESP', edicao: 330, issn: '1519-8774', ano_publi: 2023, editora_id: 2, categoria_id: 4, is_active: true },
        { id: 8, titulo: 'Revista Brasileira de Poesia', edicao: 12, issn: '2316-1234', ano_publi: 2022, editora_id: 4, categoria_id: 2, is_active: true },
      ],
      clientes: [
        { id: 1, nome: 'Helena Duarte', cpf: '529.982.247-25', telefone: '(11) 98812-4410', rua: 'Rua das Acácias', numero: 120, complemento: 'Apto 32', bairro: 'Centro', is_active: true },
        { id: 2, nome: 'Rafael Moura', cpf: '168.995.350-09', telefone: '(21) 99701-2288', rua: 'Avenida Brasil', numero: 845, complemento: '', bairro: 'Jardim América', is_active: true },
        { id: 3, nome: 'Lívia Castro', cpf: '714.602.380-01', telefone: '(31) 98455-7301', rua: 'Rua Ipê Amarelo', numero: 18, complemento: 'Casa 2', bairro: 'Santa Mônica', is_active: true },
        { id: 4, nome: 'Tomás Pereira', cpf: '043.157.950-66', telefone: '(41) 99120-6634', rua: 'Rua do Comércio', numero: 77, complemento: '', bairro: 'Vila Nova', is_active: false },
      ],
      emprestimos: [
        { id: 1, material_id: 1, cliente_id: 1, data_emprestimo: atras(3), data_devolucao: null, status: 'ABERTO', is_active: true },
        { id: 2, material_id: 4, cliente_id: 2, data_emprestimo: atras(41), data_devolucao: null, status: 'ABERTO', is_active: true },
        { id: 3, material_id: 3, cliente_id: 3, data_emprestimo: atras(60), data_devolucao: atras(48), status: 'DEVOLVIDO', is_active: true },
        { id: 4, material_id: 7, cliente_id: 3, data_emprestimo: atras(28), data_devolucao: null, status: 'ABERTO', is_active: true },
        { id: 5, material_id: 1, cliente_id: 2, data_emprestimo: atras(90), data_devolucao: atras(75), status: 'DEVOLVIDO', is_active: true },
        { id: 6, material_id: 1, cliente_id: 3, data_emprestimo: atras(70), data_devolucao: atras(55), status: 'DEVOLVIDO', is_active: true },
        { id: 7, material_id: 2, cliente_id: 1, data_emprestimo: atras(80), data_devolucao: atras(66), status: 'DEVOLVIDO', is_active: true },
        { id: 8, material_id: 3, cliente_id: 1, data_emprestimo: atras(45), data_devolucao: atras(33), status: 'DEVOLVIDO', is_active: true },
        { id: 9, material_id: 5, cliente_id: 2, data_emprestimo: atras(50), data_devolucao: atras(40), status: 'DEVOLVIDO', is_active: true },
        { id: 10, material_id: 4, cliente_id: 3, data_emprestimo: atras(110), data_devolucao: atras(95), status: 'DEVOLVIDO', is_active: true },
      ],
      reservas: [
        { id: 1, titulo: 'Dom Casmurro', cliente_id: 3, material_id: null, data: atras(1), status: 'ABERTA', is_active: true },
        { id: 2, titulo: 'Grande sertão: veredas', cliente_id: 1, material_id: null, data: atras(12), status: 'EXPIRADA', is_active: true },
      ],
    };
    this.proximoMaterial = 9;
  }

  /** Empréstimos sem devolução depois do prazo ficam atrasados, como faz o scheduler da API. */
  atualizarStatus() {
    const limite = CONFIG.PRAZO_EMPRESTIMO_DIAS * 24 * 60 * 60 * 1000;
    for (const e of this.db.emprestimos) {
      if (!e.data_devolucao) e.status = Date.now() - new Date(e.data_emprestimo) > limite ? 'ATRASADO' : 'ABERTO';
    }
    const emprestados = new Set(this.db.emprestimos.filter((e) => !e.data_devolucao).map((e) => e.material_id));
    const reservados = new Set(this.db.reservas.filter((r) => r.status === 'ABERTA' && r.is_active).map((r) => r.titulo));
    for (const m of [...this.db.livros, ...this.db.revistas]) {
      m.status = emprestados.has(m.id) ? 'EMPRESTADO' : reservados.has(m.titulo) ? 'RESERVADO' : 'DISPONIVEL';
    }
  }

  /** Imita o MaterialRouter: catálogo geral (livros + revistas) e contagens. */
  rotaMaterial(a, b) {
    const materiais = [
      ...this.db.livros.map((m) => ({ ...m, tipo: 'livro' })),
      ...this.db.revistas.map((m) => ({ ...m, tipo: 'revista' })),
    ];
    const disponiveis = materiais.filter((m) => m.status === 'DISPONIVEL' && m.is_active);
    const agrupar = (campo) => Object.entries(materiais.reduce((acc, m) => ({ ...acc, [m[campo]]: (acc[m[campo]] || 0) + 1 }), {}));

    if (!a) return materiais;
    if (a === 'disponiveis') return disponiveis;
    if (a === 'emprestados') return materiais.filter((m) => m.status === 'EMPRESTADO');
    if (a === 'quantidade' && b === 'total') return { quantidade: materiais.length };
    if (a === 'quantidade' && b === 'disponiveis') return { quantidade: disponiveis.length };
    if (a === 'quantidade' && b === 'categoria') return agrupar('categoria_id').map(([id, quantidade]) => ({ categoria_id: Number(id), quantidade }));
    if (a === 'quantidade' && b === 'tipo') return agrupar('tipo').map(([tipo, quantidade]) => ({ tipo, quantidade }));
    throw new ApiError(404, 'Rota não encontrada.');
  }

  async requisitar(metodo, caminho, corpo) {
    await new Promise((r) => setTimeout(r, 220));
    const copia = (v) => JSON.parse(JSON.stringify(v ?? null));
    const partes = caminho.replace(/\/$/, '').split('/').filter(Boolean).map(decodeURIComponent);
    const [recurso, a, b] = partes;
    if (recurso === 'material' && metodo === 'GET') {
      this.atualizarStatus();
      return copia(this.rotaMaterial(a, b));
    }
    const tabelas = { livro: 'livros', revista: 'revistas', cliente: 'clientes', autor: 'autores', categoria: 'categorias', editora: 'editoras', emprestimo: 'emprestimos', reserva: 'reservas' };
    const lista = this.db[tabelas[recurso]];
    if (!lista) throw new ApiError(404, 'Rota não encontrada.');

    const achar = (id) => {
      const item = lista.find((i) => i.id === Number(id));
      if (!item) throw new ApiError(404, 'Registro não encontrado.');
      return item;
    };
    this.atualizarStatus();

    if (metodo === 'GET') {
      if (a === 'abertos') return copia(lista.filter((e) => !e.data_devolucao));
      if (a === 'atrasados') return copia(lista.filter((e) => e.status === 'ATRASADO'));
      if (a === 'abertas') return copia(lista.filter((r) => r.status === 'ABERTA' && r.is_active));
      if (a === 'expiradas') return copia(lista.filter((r) => r.status === 'EXPIRADA'));
      return copia(lista);
    }

    if (metodo === 'POST') {
      const novo = { ...corpo, is_active: true };
      if (recurso === 'livro' || recurso === 'revista') {
        novo.id = this.proximoMaterial++;
      } else {
        novo.id = Math.max(0, ...lista.map((i) => i.id)) + 1;
      }
      if (recurso === 'emprestimo') {
        const emprestado = this.db.emprestimos.some((e) => e.material_id === novo.material_id && !e.data_devolucao);
        if (emprestado) throw new ApiError(400, 'Este material já está emprestado.');
        Object.assign(novo, { data_emprestimo: new Date().toISOString(), data_devolucao: null, status: 'ABERTO' });
      }
      if (recurso === 'reserva') {
        Object.assign(novo, { material_id: null, data: new Date().toISOString(), status: 'ABERTA' });
      }
      lista.push(novo);
      return copia(novo);
    }

    if (metodo === 'PATCH') {
      if (a === 'ativar') { achar(b).is_active = true; return { mensagem: 'Ativado' }; }
      if (b === 'ativar') { achar(a).is_active = true; return { mensagem: 'Ativado' }; }
      if (b === 'inativar') { achar(a).is_active = false; return { mensagem: 'Inativado' }; }
      const item = achar(a);
      if (recurso === 'autor' || recurso === 'editora') { item.nome = corpo.nome; return copia(item); }
      if (recurso === 'emprestimo') { item.data_devolucao = new Date().toISOString(); item.status = 'DEVOLVIDO'; return copia(item); }
      if (recurso === 'reserva' && b === 'cancelar') { item.is_active = false; item.status = 'CANCELADA'; return copia(item); }
      if (recurso === 'reserva') { item.status = 'ATENDIDA'; return copia(item); }
      for (const [k, v] of Object.entries(corpo || {})) if (v !== null && v !== undefined) item[k] = v;
      return copia(item);
    }

    if (metodo === 'DELETE') {
      const item = achar(a);
      item.is_active = false;
      return { mensagem: 'Inativado' };
    }

    throw new ApiError(405, 'Método não suportado.');
  }
}
