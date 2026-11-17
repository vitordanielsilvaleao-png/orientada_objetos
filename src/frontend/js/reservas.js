// Tela de Reservas: nova reserva por título, lista com filtros, atender e cancelar.

let reservas = [];
let filtroReservas = "abertas";

const CAMINHOS_RESERVA = {
  abertas: "/reserva/abertas",
  expiradas: "/reserva/expiradas",
  todas: "/reserva",
};

async function carregarReservas() {
  const tbody = document.getElementById("tabelaReservas");
  linhaCarregando(tbody, 7);
  await carregarApoio();

  preencherSelect("resCliente", clientes.filter((c) => c.is_active), (c) => formatarNome(c.nome));
  preencherSugestoesTitulo();

  const { ok, data } = await chamarApi("GET", CAMINHOS_RESERVA[filtroReservas]);
  if (!ok) {
    linhaVazia(tbody, 7, mensagemDeErro(data, "Não foi possível carregar as reservas."));
    return;
  }
  reservas = data;
  renderizarReservas();
}

// Sugere os títulos do acervo, sem repetir (pode haver vários exemplares do mesmo título)
function preencherSugestoesTitulo() {
  const titulos = [...new Set(materiais.filter((m) => m.is_active).map((m) => capitalizar(m.titulo)))];
  document.getElementById("listaTitulos").innerHTML =
    titulos.map((t) => `<option value="${esc(t)}">`).join("");
}

// Compara do jeito do back-end: sem espaços nas pontas e em minúsculas (acento conta)
function tituloNoAcervo(titulo) {
  const procurado = titulo.trim().toLowerCase();
  return materiais.some((m) => m.is_active && m.titulo === procurado);
}

function renderizarReservas() {
  const tbody = document.getElementById("tabelaReservas");
  const termo = document.getElementById("buscaReservas").value;

  const lista = reservas.filter((r) => combinaComBusca([r.titulo, nomePorId(clientes, r.cliente_id)], termo));

  if (lista.length === 0) {
    const vazio = { abertas: "Nenhuma reserva aguardando atendimento.", expiradas: "Nenhuma reserva expirada.", todas: "Nenhuma reserva registrada ainda." };
    linhaVazia(tbody, 7, termo.trim() ? `Nada encontrado para "${termo.trim()}".` : vazio[filtroReservas]);
    document.getElementById("contagemReservas").textContent = "";
    return;
  }

  tbody.innerHTML = "";
  const template = document.getElementById("linhaReservaTemplate");

  lista.forEach((reserva) => {
    const node = template.content.cloneNode(true);
    node.querySelector(".t-id").textContent = reserva.id;
    node.querySelector(".t-titulo").textContent = capitalizar(reserva.titulo);
    node.querySelector(".t-cliente").textContent = nomePorId(clientes, reserva.cliente_id);
    node.querySelector(".t-data").textContent = formatarData(reserva.data);
    let exemplar = "Aguardando devolução";
    if (reserva.material_id) exemplar = `Separado (nº ${reserva.material_id})`;
    else if (!tituloNoAcervo(reserva.titulo)) exemplar = "Fora do acervo";
    node.querySelector(".t-exemplar").textContent = exemplar;
    aplicarSelo(node.querySelector(".t-status"), reserva.status);

    const atender = node.querySelector(".b-atender");
    const cancelar = node.querySelector(".b-cancelar");
    if (!reserva.is_active) {
      atender.remove();
      cancelar.remove();
    } else {
      // Só dá para atender quando já existe um exemplar vinculado à reserva
      if (reserva.material_id) {
        atender.addEventListener("click", () => atenderReserva(reserva));
      } else {
        atender.remove();
      }
      cancelar.addEventListener("click", () => cancelarReserva(reserva));
    }
    tbody.appendChild(node);
  });

  document.getElementById("contagemReservas").textContent = plural(lista.length, "reserva", "reservas");
}

document.getElementById("formReserva").addEventListener("submit", async (e) => {
  e.preventDefault();
  limparInvalidos(e.target);
  if (!exigirSelecao("resCliente", "o cliente")) return;
  if (!exigirTexto("resTitulo", "o título")) return;

  // Título fora do acervo também pode ser reservado: quando o livro ou a revista for
  // cadastrado, o LivroService/RevistaService vincula o exemplar à reserva mais antiga
  const titulo = document.getElementById("resTitulo").value.trim();
  const existeNoAcervo = tituloNoAcervo(titulo);

  const payload = {
    cliente_id: parseInt(document.getElementById("resCliente").value, 10),
    titulo,
  };

  await comBotaoOcupado(e.target, async () => {
    const { ok, data } = await chamarApi("POST", "/reserva", payload);
    if (!ok) {
      showToast(mensagemDeErro(data, "Erro ao fazer a reserva."), "err");
      return;
    }
    let mensagem = "Reserva feita. O cliente entra na fila até um exemplar ser devolvido.";
    if (data.material_id) {
      mensagem = "Reserva feita. Havia um exemplar disponível, e ele já ficou separado.";
    } else if (!existeNoAcervo) {
      mensagem = "Reserva feita. O título ainda não está no acervo: o exemplar será separado quando ele for cadastrado.";
    }
    showToast(mensagem, "ok");
    e.target.reset();
    carregarReservas();
  });
});

async function atenderReserva(reserva) {
  const confirmou = await pedirConfirmacao(
    "Atender reserva?",
    `Registra o empréstimo de "${capitalizar(reserva.titulo)}" para ${nomePorId(clientes, reserva.cliente_id)} e encerra a reserva.`,
    "Atender reserva",
  );
  if (!confirmou) return;

  const { ok, data } = await chamarApi("PATCH", `/reserva/${reserva.id}`);
  if (!ok) {
    showToast(mensagemDeErro(data, "Erro ao atender a reserva."), "err");
    return;
  }
  showToast("Reserva atendida e empréstimo registrado.", "ok");
  carregarReservas();
}

async function cancelarReserva(reserva) {
  const confirmou = await pedirConfirmacao(
    "Cancelar reserva?",
    `A reserva de "${capitalizar(reserva.titulo)}" para ${nomePorId(clientes, reserva.cliente_id)} será encerrada.`,
    "Cancelar reserva",
    true,
  );
  if (!confirmou) return;

  const { ok, data } = await chamarApi("PATCH", `/reserva/${reserva.id}/cancelar`);
  if (!ok) {
    showToast(mensagemDeErro(data, "Erro ao cancelar a reserva."), "err");
    return;
  }
  showToast("Reserva cancelada.", "ok");
  carregarReservas();
}

document.querySelectorAll("[data-filtro-res]").forEach((aba) => {
  aba.addEventListener("click", () => {
    filtroReservas = aba.dataset.filtroRes;
    document.querySelectorAll("[data-filtro-res]").forEach((a) => {
      a.setAttribute("aria-selected", String(a === aba));
    });
    carregarReservas();
  });
});

document.getElementById("buscaReservas").addEventListener("input", renderizarReservas);
