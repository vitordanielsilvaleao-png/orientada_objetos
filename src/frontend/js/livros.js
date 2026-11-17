// Tela de Livros: cadastro, lista, edição, inativação e reativação.

let livros = [];

async function carregarLivros() {
  const tbody = document.getElementById("tabelaLivros");
  linhaCarregando(tbody, 8);
  await carregarApoio();
  preencherSelectsLivro();

  const { ok, data } = await chamarApi("GET", "/livro");
  if (!ok) {
    linhaVazia(tbody, 8, mensagemDeErro(data, "Não foi possível carregar os livros."));
    return;
  }
  livros = data;
  renderizarLivros();
}

function preencherSelectsLivro() {
  const porNome = (i) => formatarNome(i.nome);
  preencherSelect("livroAutor", autores, porNome);
  preencherSelect("livroEditora", editoras, porNome);
  preencherSelect("livroCategoria", categorias, porNome);
  preencherSelect("editLivroAutor", autores, porNome);
  preencherSelect("editLivroEditora", editoras, porNome);
  preencherSelect("editLivroCategoria", categorias, porNome);
}

function renderizarLivros() {
  const tbody = document.getElementById("tabelaLivros");
  const termo = document.getElementById("buscaLivros").value;
  const mostrarInativos = document.getElementById("inativosLivros").checked;

  const lista = livros.filter((l) =>
    (mostrarInativos || l.is_active) &&
    combinaComBusca([l.titulo, l.isbn, nomePorId(autores, l.autor_id)], termo));

  if (lista.length === 0) {
    linhaVazia(tbody, 8, termo.trim() ? `Nenhum livro encontrado para "${termo.trim()}".` : "Nenhum livro cadastrado ainda.");
    document.getElementById("contagemLivros").textContent = "";
    return;
  }

  tbody.innerHTML = "";
  const template = document.getElementById("linhaLivroTemplate");

  lista.forEach((livro) => {
    const node = template.content.cloneNode(true);
    node.querySelector("tr").classList.toggle("inativa", !livro.is_active);
    node.querySelector(".t-titulo").textContent = capitalizar(livro.titulo);
    node.querySelector(".t-detalhe").textContent = `ISBN ${livro.isbn}`;
    node.querySelector(".t-autor").textContent = nomePorId(autores, livro.autor_id);
    node.querySelector(".t-editora").textContent = nomePorId(editoras, livro.editora_id);
    node.querySelector(".t-categoria").textContent = nomePorId(categorias, livro.categoria_id);
    node.querySelector(".t-ano").textContent = livro.ano_publi;
    aplicarSelo(node.querySelector(".t-status"), livro.status);
    aplicarSeloAtivo(node.querySelector(".t-situacao"), livro.is_active);

    node.querySelector(".b-editar").addEventListener("click", () => abrirEdicaoLivro(livro));

    const botaoAtivacao = node.querySelector(".b-ativacao");
    if (livro.is_active) {
      botaoAtivacao.title = "Inativar";
      botaoAtivacao.classList.add("perigo");
      botaoAtivacao.addEventListener("click", () => inativarLivro(livro));
    } else {
      botaoAtivacao.title = "Reativar";
      botaoAtivacao.innerHTML = '<i class="fa-solid fa-power-off"></i>';
      botaoAtivacao.addEventListener("click", () => ativarLivro(livro));
    }
    botaoAtivacao.setAttribute("aria-label", botaoAtivacao.title);

    tbody.appendChild(node);
  });

  const ocultos = livros.length - lista.length;
  document.getElementById("contagemLivros").textContent =
    plural(lista.length, "livro", "livros") + (ocultos && !termo.trim() ? ` (${ocultos} inativo(s) oculto(s))` : "");
}

// Validação própria antes de enviar (o back-end valida de novo)
function validarFormLivro() {
  limparInvalidos(document.getElementById("formLivro"));
  if (!exigirTexto("livroTitulo", "o título")) return false;
  if (somenteDigitos(document.getElementById("livroIsbn").value).length !== 13) {
    return campoInvalido("livroIsbn", "ISBN: informe os 13 dígitos (pontos e hífens são aceitos).");
  }
  if (!exigirAno("livroAno")) return false;
  if (!exigirSelecao("livroAutor", "o autor")) return false;
  if (!exigirSelecao("livroEditora", "a editora")) return false;
  return exigirSelecao("livroCategoria", "a categoria");
}

document.getElementById("formLivro").addEventListener("submit", async (e) => {
  e.preventDefault();
  if (!validarFormLivro()) return;

  const payload = {
    titulo: document.getElementById("livroTitulo").value.trim(),
    isbn: document.getElementById("livroIsbn").value.trim(),
    ano_publi: parseInt(document.getElementById("livroAno").value, 10),
    autor_id: parseInt(document.getElementById("livroAutor").value, 10),
    editora_id: parseInt(document.getElementById("livroEditora").value, 10),
    categoria_id: parseInt(document.getElementById("livroCategoria").value, 10),
  };

  await comBotaoOcupado(e.target, async () => {
    const { ok, data } = await chamarApi("POST", "/livro", payload);
    if (!ok) {
      showToast(mensagemDeErro(data, "Erro ao cadastrar o livro."), "err");
      return;
    }
    showToast(`Livro "${capitalizar(data.titulo)}" cadastrado!`, "ok");
    e.target.reset();
    carregarLivros();
  });
});

function abrirEdicaoLivro(livro) {
  if (!livro.is_active) {
    showToast("Reative o livro antes de editar: material inativo não pode ser atualizado.", "err");
    return;
  }
  document.getElementById("editLivroId").value = livro.id;
  document.getElementById("editLivroIsbn").textContent = `ISBN ${livro.isbn}`;
  document.getElementById("editLivroTitulo").value = capitalizar(livro.titulo);
  document.getElementById("editLivroAno").value = livro.ano_publi;
  document.getElementById("editLivroAutor").value = livro.autor_id;
  document.getElementById("editLivroEditora").value = livro.editora_id;
  document.getElementById("editLivroCategoria").value = livro.categoria_id;
  abrirModal("modalLivro");
}

document.getElementById("formEditarLivro").addEventListener("submit", async (e) => {
  e.preventDefault();
  limparInvalidos(e.target);
  if (!exigirTexto("editLivroTitulo", "o título") || !exigirAno("editLivroAno")) return;

  const id = document.getElementById("editLivroId").value;
  const payload = {
    titulo: document.getElementById("editLivroTitulo").value.trim(),
    ano_publi: parseInt(document.getElementById("editLivroAno").value, 10),
    autor_id: parseInt(document.getElementById("editLivroAutor").value, 10),
    editora_id: parseInt(document.getElementById("editLivroEditora").value, 10),
    categoria_id: parseInt(document.getElementById("editLivroCategoria").value, 10),
  };

  await comBotaoOcupado(e.target, async () => {
    const { ok, data } = await chamarApi("PATCH", `/livro/${id}`, payload);
    if (!ok) {
      showToast(mensagemDeErro(data, "Erro ao editar o livro."), "err");
      return;
    }
    showToast("Livro atualizado com sucesso!", "ok");
    fecharModal("modalLivro");
    carregarLivros();
  });
});

async function inativarLivro(livro) {
  const confirmou = await pedirConfirmacao(
    "Inativar livro?",
    `"${capitalizar(livro.titulo)}" deixa de ficar disponível para empréstimos. Você pode reativá-lo depois.`,
    "Inativar livro",
    true,
  );
  if (!confirmou) return;

  const { ok, data } = await chamarApi("PATCH", `/livro/${livro.id}/inativar`);
  if (!ok) {
    showToast(mensagemDeErro(data, "Erro ao inativar o livro."), "err");
    return;
  }
  showToast("Livro inativado.", "ok");
  carregarLivros();
}

async function ativarLivro(livro) {
  const { ok, data } = await chamarApi("PATCH", `/livro/${livro.id}/ativar`);
  if (!ok) {
    showToast(mensagemDeErro(data, "Erro ao reativar o livro."), "err");
    return;
  }
  showToast("Livro reativado.", "ok");
  carregarLivros();
}

document.getElementById("buscaLivros").addEventListener("input", renderizarLivros);
document.getElementById("inativosLivros").addEventListener("change", renderizarLivros);
