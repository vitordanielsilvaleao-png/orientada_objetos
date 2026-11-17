// Tela de Revistas: cadastro, lista, edição, inativação e reativação.

let revistas = [];

async function carregarRevistas() {
  const tbody = document.getElementById("tabelaRevistas");
  linhaCarregando(tbody, 8);
  await carregarApoio();
  preencherSelectsRevista();

  const { ok, data } = await chamarApi("GET", "/revista");
  if (!ok) {
    linhaVazia(tbody, 8, mensagemDeErro(data, "Não foi possível carregar as revistas."));
    return;
  }
  revistas = data;
  renderizarRevistas();
}

function preencherSelectsRevista() {
  const porNome = (i) => formatarNome(i.nome);
  preencherSelect("revistaEditora", editoras, porNome);
  preencherSelect("revistaCategoria", categorias, porNome);
  preencherSelect("editRevistaEditora", editoras, porNome);
  preencherSelect("editRevistaCategoria", categorias, porNome);
}

function formatarIssn(issn) {
  return issn && issn.length === 8 ? `${issn.slice(0, 4)}-${issn.slice(4)}` : issn;
}

function renderizarRevistas() {
  const tbody = document.getElementById("tabelaRevistas");
  const termo = document.getElementById("buscaRevistas").value;
  const mostrarInativas = document.getElementById("inativosRevistas").checked;

  const lista = revistas.filter((r) =>
    (mostrarInativas || r.is_active) &&
    combinaComBusca([r.titulo, r.issn, formatarIssn(r.issn), r.edicao], termo));

  if (lista.length === 0) {
    linhaVazia(tbody, 8, termo.trim() ? `Nenhuma revista encontrada para "${termo.trim()}".` : "Nenhuma revista cadastrada ainda.");
    document.getElementById("contagemRevistas").textContent = "";
    return;
  }

  tbody.innerHTML = "";
  // A linha da revista tem as mesmas colunas da do livro; só muda o conteúdo da 2ª
  const template = document.getElementById("linhaLivroTemplate");

  lista.forEach((revista) => {
    const node = template.content.cloneNode(true);
    node.querySelector("tr").classList.toggle("inativa", !revista.is_active);
    node.querySelector(".t-titulo").textContent = capitalizar(revista.titulo);
    node.querySelector(".t-detalhe").textContent = `Edição ${revista.edicao}`;
    node.querySelector(".t-autor").textContent = formatarIssn(revista.issn);
    node.querySelector(".t-autor").dataset.rotulo = "ISSN";
    node.querySelector(".t-editora").textContent = nomePorId(editoras, revista.editora_id);
    node.querySelector(".t-categoria").textContent = nomePorId(categorias, revista.categoria_id);
    node.querySelector(".t-ano").textContent = revista.ano_publi;
    aplicarSelo(node.querySelector(".t-status"), revista.status);
    aplicarSeloAtivo(node.querySelector(".t-situacao"), revista.is_active);

    node.querySelector(".b-editar").addEventListener("click", () => abrirEdicaoRevista(revista));

    const botaoAtivacao = node.querySelector(".b-ativacao");
    if (revista.is_active) {
      botaoAtivacao.title = "Inativar";
      botaoAtivacao.classList.add("perigo");
      botaoAtivacao.addEventListener("click", () => inativarRevista(revista));
    } else {
      botaoAtivacao.title = "Reativar";
      botaoAtivacao.innerHTML = '<i class="fa-solid fa-power-off"></i>';
      botaoAtivacao.addEventListener("click", () => ativarRevista(revista));
    }
    botaoAtivacao.setAttribute("aria-label", botaoAtivacao.title);

    tbody.appendChild(node);
  });

  const ocultas = revistas.length - lista.length;
  document.getElementById("contagemRevistas").textContent =
    plural(lista.length, "revista", "revistas") + (ocultas && !termo.trim() ? ` (${ocultas} inativa(s) oculta(s))` : "");
}

function validarFormRevista() {
  limparInvalidos(document.getElementById("formRevista"));
  if (!exigirTexto("revistaTitulo", "o título")) return false;
  if (!exigirInteiroPositivo("revistaEdicao", "Edição")) return false;
  if (somenteDigitos(document.getElementById("revistaIssn").value).length !== 8) {
    return campoInvalido("revistaIssn", "ISSN: informe os 8 dígitos, com ou sem hífen (ex.: 0104-1789).");
  }
  if (!exigirAno("revistaAno")) return false;
  if (!exigirSelecao("revistaEditora", "a editora")) return false;
  return exigirSelecao("revistaCategoria", "a categoria");
}

document.getElementById("formRevista").addEventListener("submit", async (e) => {
  e.preventDefault();
  if (!validarFormRevista()) return;

  const payload = {
    titulo: document.getElementById("revistaTitulo").value.trim(),
    edicao: parseInt(document.getElementById("revistaEdicao").value, 10),
    issn: document.getElementById("revistaIssn").value.trim(),
    ano_publi: parseInt(document.getElementById("revistaAno").value, 10),
    editora_id: parseInt(document.getElementById("revistaEditora").value, 10),
    categoria_id: parseInt(document.getElementById("revistaCategoria").value, 10),
  };

  await comBotaoOcupado(e.target, async () => {
    const { ok, data } = await chamarApi("POST", "/revista", payload);
    if (!ok) {
      showToast(mensagemDeErro(data, "Erro ao cadastrar a revista."), "err");
      return;
    }
    showToast(`Revista "${capitalizar(data.titulo)}" cadastrada!`, "ok");
    e.target.reset();
    carregarRevistas();
  });
});

function abrirEdicaoRevista(revista) {
  if (!revista.is_active) {
    showToast("Reative a revista antes de editar: material inativo não pode ser atualizado.", "err");
    return;
  }
  document.getElementById("editRevistaId").value = revista.id;
  document.getElementById("editRevistaIssn").textContent = `ISSN ${formatarIssn(revista.issn)}`;
  document.getElementById("editRevistaTitulo").value = capitalizar(revista.titulo);
  document.getElementById("editRevistaEdicao").value = revista.edicao;
  document.getElementById("editRevistaAno").value = revista.ano_publi;
  document.getElementById("editRevistaEditora").value = revista.editora_id;
  document.getElementById("editRevistaCategoria").value = revista.categoria_id;
  abrirModal("modalRevista");
}

document.getElementById("formEditarRevista").addEventListener("submit", async (e) => {
  e.preventDefault();
  limparInvalidos(e.target);
  if (!exigirTexto("editRevistaTitulo", "o título") ||
      !exigirInteiroPositivo("editRevistaEdicao", "Edição") ||
      !exigirAno("editRevistaAno")) return;

  const id = document.getElementById("editRevistaId").value;
  const payload = {
    titulo: document.getElementById("editRevistaTitulo").value.trim(),
    edicao: parseInt(document.getElementById("editRevistaEdicao").value, 10),
    ano_publi: parseInt(document.getElementById("editRevistaAno").value, 10),
    editora_id: parseInt(document.getElementById("editRevistaEditora").value, 10),
    categoria_id: parseInt(document.getElementById("editRevistaCategoria").value, 10),
  };

  await comBotaoOcupado(e.target, async () => {
    const { ok, data } = await chamarApi("PATCH", `/revista/${id}`, payload);
    if (!ok) {
      showToast(mensagemDeErro(data, "Erro ao editar a revista."), "err");
      return;
    }
    showToast("Revista atualizada com sucesso!", "ok");
    fecharModal("modalRevista");
    carregarRevistas();
  });
});

async function inativarRevista(revista) {
  const confirmou = await pedirConfirmacao(
    "Inativar revista?",
    `"${capitalizar(revista.titulo)}" deixa de ficar disponível para empréstimos. Você pode reativá-la depois.`,
    "Inativar revista",
    true,
  );
  if (!confirmou) return;

  const { ok, data } = await chamarApi("PATCH", `/revista/${revista.id}/inativar`);
  if (!ok) {
    showToast(mensagemDeErro(data, "Erro ao inativar a revista."), "err");
    return;
  }
  showToast("Revista inativada.", "ok");
  carregarRevistas();
}

async function ativarRevista(revista) {
  const { ok, data } = await chamarApi("PATCH", `/revista/${revista.id}/ativar`);
  if (!ok) {
    showToast(mensagemDeErro(data, "Erro ao reativar a revista."), "err");
    return;
  }
  showToast("Revista reativada.", "ok");
  carregarRevistas();
}

document.getElementById("buscaRevistas").addEventListener("input", renderizarRevistas);
document.getElementById("inativosRevistas").addEventListener("change", renderizarRevistas);
