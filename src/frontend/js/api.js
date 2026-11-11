/**
 * Camada de comunicação com a API.
 * Todas as telas falam com o back-end apenas através desta classe.
 */

/** Nomes amigáveis dos campos, usados para traduzir erros de validação (422). */
const NOMES_CAMPOS = {
  titulo: 'Título', ano_publi: 'Ano de publicação', categoria_id: 'Categoria',
  editora_id: 'Editora', autor_id: 'Autor', isbn: 'ISBN', issn: 'ISSN', edicao: 'Edição',
  nome: 'Nome', bairro: 'Bairro', rua: 'Rua', numero: 'Número', complemento: 'Complemento',
  telefone: 'Telefone', material_id: 'Material', cliente_id: 'Cliente',
};

class ApiError extends Error {
  constructor(status, mensagem, detalhes = null) {
    super(mensagem);
    this.name = 'ApiError';
    this.status = status;
    this.detalhes = detalhes;
  }
}

class ApiClient {
  constructor(baseUrl) {
    this.baseUrl = baseUrl.replace(/\/$/, '');
  }

  get(caminho) { return this.requisitar('GET', caminho); }
  post(caminho, corpo) { return this.requisitar('POST', caminho, corpo); }
  patch(caminho, corpo) { return this.requisitar('PATCH', caminho, corpo); }
  delete(caminho) { return this.requisitar('DELETE', caminho); }

  async requisitar(metodo, caminho, corpo) {
    const opcoes = { method: metodo, headers: { Accept: 'application/json' } };
    if (corpo !== undefined) {
      opcoes.headers['Content-Type'] = 'application/json';
      opcoes.body = JSON.stringify(corpo);
    }

    let resposta;
    try {
      resposta = await fetch(this.baseUrl + caminho, opcoes);
    } catch {
      throw new ApiError(0, `Não foi possível conectar à API em ${this.baseUrl}. Verifique se o servidor está rodando e se o CORS está liberado.`);
    }

    const texto = await resposta.text();
    let dados = null;
    try { dados = texto ? JSON.parse(texto) : null; } catch { dados = texto; }

    if (!resposta.ok) {
      throw new ApiError(resposta.status, ApiClient.extrairMensagem(dados, resposta.status), dados);
    }
    return dados;
  }

  /** Converte a resposta de erro da API em uma frase legível. */
  static extrairMensagem(dados, status) {
    // Erros de validação do FastAPI (422): lista de { loc, msg }
    if (dados && Array.isArray(dados.detail) && dados.detail.every((d) => d && d.msg)) {
      return dados.detail.map((d) => {
        const campo = Array.isArray(d.loc) ? d.loc[d.loc.length - 1] : '';
        const rotulo = NOMES_CAMPOS[campo] || campo;
        return rotulo ? `${rotulo}: ${d.msg}` : d.msg;
      }).join('; ');
    }

    // Exceções do back-end (400, 404, 409...): procura o texto em qualquer formato
    const texto = ApiClient.procurarTexto(dados);
    if (texto) return texto;

    console.warn(`[API] Erro ${status} sem mensagem reconhecida. Corpo recebido:`, dados);
    const padrao = {
      400: 'A API recusou os dados enviados.',
      404: 'Registro não encontrado.',
      409: 'A operação entra em conflito com um registro existente.',
      500: 'Erro interno no servidor.',
    };
    return `${padrao[status] || 'A API respondeu com erro.'} (erro ${status})`;
  }

  /**
   * Procura a mensagem de erro dentro da resposta, aceitando formatos como:
   * "texto", { detail: "texto" }, { detail: { mensagem: "texto" } },
   * { erro: "texto" }, { message: "texto" }, { errors: ["texto"] } etc.
   */
  static procurarTexto(valor, profundidade = 0) {
    if (typeof valor === 'string') {
      const t = valor.trim();
      return t && !t.startsWith('<') ? t : null; // ignora páginas HTML de erro
    }
    if (!valor || typeof valor !== 'object' || profundidade > 4) return null;

    if (Array.isArray(valor)) {
      const textos = valor.map((v) => ApiClient.procurarTexto(v, profundidade + 1)).filter(Boolean);
      return textos.length ? textos.join('; ') : null;
    }

    const preferidas = ['detail', 'detalhe', 'mensagem', 'message', 'msg', 'erro', 'error', 'errors', 'descricao', 'description'];
    for (const chave of preferidas) {
      if (chave in valor) {
        const t = ApiClient.procurarTexto(valor[chave], profundidade + 1);
        if (t) return t;
      }
    }
    for (const [chave, v] of Object.entries(valor)) {
      if (['status', 'status_code', 'code', 'codigo'].includes(chave)) continue;
      const t = ApiClient.procurarTexto(v, profundidade + 1);
      if (t) return t;
    }
    return null;
  }

  /** As rotas GET podem devolver uma lista ou um objeto que contém a lista. */
  static comoLista(dados) {
    if (Array.isArray(dados)) return dados;
    if (dados && typeof dados === 'object') {
      const lista = Object.values(dados).find(Array.isArray);
      if (lista) return lista;
    }
    return [];
  }
}
