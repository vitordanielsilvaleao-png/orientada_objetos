// Telas de Autores, Editoras e Categorias. As três funcionam igual, então o mesmo
// código atende as três: o objeto CATALOGO diz a rota, os ids da tela e os textos de cada uma.

const CATALOGO = {
  autores: {
    rota: "/autor", singular: "autor", plural: "autores", campoMaterial: "autor_id",
    form: "formAutor", campoNome: "autorNome", tabela: "tabelaAutores", busca: "buscaAutores", contagem: "contagemAutores",
  },
  editoras: {
    rota: "/editora", singular: "editora", plural: "editoras", campoMaterial: "editora_id",
    form: "formEditora", campoNome: "editoraNome", tabela: "tabelaEditoras", busca: "buscaEditoras", contagem: "contagemEditoras",
  },
  categorias: {
    rota: "/categoria", singular: "categoria", plural: "categorias", campoMaterial: "categoria_id",
    form: "formCategoria", campoNome: "categoriaNome", tabela: "tabelaCategorias", busca: "buscaCategorias", contagem: "contagemCategorias",
  },
};

let itensCatalogo = { autores: [], editoras: [], categorias: [] };
let livrosDoCatalogo = []; // /material não traz autor_id, então os autores contam pelos livros

async function carregarCatalogo(tipo) {
  const config = CATALOGO[tipo];
  const tbody = document.getElementById(config.tabela);
  linhaCarregando(tbody, 3);

  await carregarApoio();
  const [lista, livrosResp] = await Promise.all([
    chamarApi("GET", config.rota),
    tipo === "autores" ? chamarApi("GET", "/livro") : Promise.resolve({ ok: true, data: [] }),
  ]);
  livrosDoCatalogo = livrosResp.ok ? livrosResp.data : [];

  if (!lista.ok) {
    linhaVazia(tbody, 3, mensagemDeErro(lista.data, `Não foi possível carregar ${config.plural}.`));
    return;
  }
  itensCatalogo[tipo] = lista.data;
  renderizarCatalogo(tipo);
}

function contarTitulos(tipo, id) {
  const config = CATALOGO[tipo];
  const fonte = tipo === "autores" ? livrosDoCatalogo : materiais;
  return fonte.filter((m) => m[config.campoMaterial] === id).length;
}

function renderizarCatalogo(tipo) {
  const config = CATALOGO[tipo];
  const tbody = document.getElementById(config.tabela);
  const termo = document.getElementById(config.busca).value;

  const lista = itensCatalogo[tipo]
    .filter((i) => combinaComBusca([i.nome], termo))
    .sort((a, b) => a.nome.localeCompare(b.nome, "pt-BR"));

  if (lista.length === 0) {
    linhaVazia(tbody, 3, termo.trim() ? `Nada encontrado para "${termo.trim()}".` : `Nenhum(a) ${config.singular} cadastrado(a) ainda.`);
    document.getElementById(config.contagem).textContent = "";
    return;
  }

  tbody.innerHTML = "";
  const template = document.getElementById("linhaCatalogoTemplate");

  lista.forEach((item) => {
    const node = template.content.cloneNode(true);
    node.querySelector(".t-nome").textContent = formatarNome(item.nome);
    node.querySelector(".t-quantidade").textContent = contarTitulos(tipo, item.id);
    node.querySelector(".b-editar").addEventListener("click", () => abrirRenomear(tipo, item));
    tbody.appendChild(node);
  });

  document.getElementById(config.contagem).textContent = plural(lista.length, config.singular, config.plural);
}

function abrirRenomear(tipo, item) {
  document.getElementById("editNomeTitulo").textContent = `Renomear ${CATALOGO[tipo].singular}`;
  document.getElementById("editNomeId").value = item.id;
  document.getElementById("editNomeTipo").value = tipo;
  document.getElementById("editNomeValor").value = formatarNome(item.nome);
  abrirModal("modalNome");
}

// Liga o formulário de cadastro e a busca de cada uma das três telas
Object.keys(CATALOGO).forEach((tipo) => {
  const config = CATALOGO[tipo];

  document.getElementById(config.form).addEventListener("submit", async (e) => {
    e.preventDefault();
    limparInvalidos(e.target);
    if (!exigirTexto(config.campoNome, "o nome")) return;

    const nome = document.getElementById(config.campoNome).value.trim();
    const repetido = itensCatalogo[tipo].some((i) => i.nome.trim().toLowerCase() === nome.toLowerCase());
    if (repetido) {
      campoInvalido(config.campoNome, `Já existe ${config.singular === "autor" ? "um autor" : "uma " + config.singular} com o nome "${nome}".`);
      return;
    }

    await comBotaoOcupado(e.target, async () => {
      const { ok, data } = await chamarApi("POST", config.rota, { nome });
      if (!ok) {
        showToast(mensagemDeErro(data, `Erro ao cadastrar ${config.singular}.`), "err");
        return;
      }
      showToast(`"${formatarNome(data.nome)}" cadastrado(a)!`, "ok");
      e.target.reset();
      carregarCatalogo(tipo);
    });
  });

  document.getElementById(config.busca).addEventListener("input", () => renderizarCatalogo(tipo));
});

document.getElementById("formEditarNome").addEventListener("submit", async (e) => {
  e.preventDefault();
  limparInvalidos(e.target);
  if (!exigirTexto("editNomeValor", "o nome")) return;

  const tipo = document.getElementById("editNomeTipo").value;
  const id = document.getElementById("editNomeId").value;
  const nome = document.getElementById("editNomeValor").value.trim();

  await comBotaoOcupado(e.target, async () => {
    const { ok, data } = await chamarApi("PATCH", `${CATALOGO[tipo].rota}/${id}`, { nome });
    if (!ok) {
      showToast(mensagemDeErro(data, "Erro ao salvar o nome."), "err");
      return;
    }
    showToast("Nome salvo.", "ok");
    fecharModal("modalNome");
    carregarCatalogo(tipo);
  });
});
