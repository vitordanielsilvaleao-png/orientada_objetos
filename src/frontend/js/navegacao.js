// Menu lateral: mostra uma seção por vez conforme o endereço (#livros, #clientes...),
// abre e fecha o menu no celular, controla as janelas e verifica se a API está no ar.

// Cada item do menu aponta para a função que carrega a sua tela
const SECOES = {
  painel: { titulo: "Painel", carregar: carregarPainel },
  livros: { titulo: "Livros", carregar: carregarLivros },
  revistas: { titulo: "Revistas", carregar: carregarRevistas },
  emprestimos: { titulo: "Empréstimos", carregar: carregarEmprestimos },
  reservas: { titulo: "Reservas", carregar: carregarReservas },
  relatorios: { titulo: "Relatórios", carregar: carregarRelatorios },
  clientes: { titulo: "Clientes", carregar: carregarClientes },
  autores: { titulo: "Autores", carregar: () => carregarCatalogo("autores") },
  editoras: { titulo: "Editoras", carregar: () => carregarCatalogo("editoras") },
  categorias: { titulo: "Categorias", carregar: () => carregarCatalogo("categorias") },
};

function mostrarSecao() {
  const pedida = window.location.hash.replace("#", "");
  const nome = SECOES[pedida] ? pedida : "painel";

  document.querySelectorAll(".secao").forEach((secao) => {
    secao.hidden = secao.id !== `secao-${nome}`;
  });
  document.querySelectorAll(".menu-item").forEach((item) => {
    const atual = item.dataset.secao === nome;
    item.classList.toggle("ativo", atual);
    if (atual) item.setAttribute("aria-current", "page");
    else item.removeAttribute("aria-current");
  });

  document.title = `${SECOES[nome].titulo} | Apolo`;
  alternarMenu(false);
  window.scrollTo(0, 0);
  SECOES[nome].carregar();
}

window.addEventListener("hashchange", mostrarSecao);

// Links que já abrem Empréstimos na aba "Atrasados" (no Painel)
document.addEventListener("click", (e) => {
  const link = e.target.closest("[data-filtro-destino]");
  if (link) definirFiltroEmprestimos(link.dataset.filtroDestino);
});

// ---------- Menu no celular ----------

function alternarMenu(abrir) {
  document.getElementById("barra").classList.toggle("aberta", abrir);
  document.getElementById("fundoMenu").hidden = !abrir;
  document.getElementById("btnAbrirMenu").setAttribute("aria-expanded", String(abrir));
}

document.getElementById("btnAbrirMenu").addEventListener("click", () => alternarMenu(true));
document.getElementById("fundoMenu").addEventListener("click", () => alternarMenu(false));

// ---------- Janelas ----------

// Botões com data-fechar="idDaJanela"
document.querySelectorAll("[data-fechar]").forEach((botao) => {
  botao.addEventListener("click", () => fecharModal(botao.dataset.fechar));
});

// Clicar fora da janela fecha
document.querySelectorAll(".sobreposicao").forEach((fundo) => {
  fundo.addEventListener("click", (e) => {
    if (e.target === fundo) fecharModal(fundo.id);
  });
});

document.addEventListener("keydown", (e) => {
  if (e.key !== "Escape") return;
  alternarMenu(false);
  document.querySelectorAll(".sobreposicao.show").forEach((fundo) => fecharModal(fundo.id));
});

document.getElementById("btnConceitos").addEventListener("click", () => {
  alternarMenu(false);
  abrirModal("modalConceitos");
});

// ---------- Início ----------

(function init() {
  mostrarSecao();
})();
