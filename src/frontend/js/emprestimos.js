// Tela de Empréstimos: registro em 2 etapas (cliente → material), lista com filtros e devolução.

const LIMITE_EMPRESTIMOS = 4; // o mesmo limite do EmprestimoService.cadastrar()

let emprestimos = [];       // lista da aba escolhida
let todosEmprestimos = [];  // usada para contar os empréstimos ativos de cada cliente
let reservasAtivas = [];    // usada para liberar o material RESERVADO para quem reservou
let filtroEmprestimos = "abertos";
let clienteEmprestimo = null;

const CAMINHOS_EMPRESTIMO = {
  abertos: "/emprestimo/abertos",
  atrasados: "/emprestimo/atrasados",
  todos: "/emprestimo",
};

async function carregarEmprestimos() {
  const tbody = document.getElementById("tabelaEmprestimos");
  linhaCarregando(tbody, 8);
  await carregarApoio();

  const [lista, todos, reservas] = await Promise.all([
    chamarApi("GET", CAMINHOS_EMPRESTIMO[filtroEmprestimos]),
    chamarApi("GET", "/emprestimo"),
    chamarApi("GET", "/reserva/abertas"),
  ]);
  todosEmprestimos = todos.ok ? todos.data : [];
  reservasAtivas = reservas.ok ? reservas.data : [];

  preencherSelect("empCliente", clientes.filter((c) => c.is_active), (c) => formatarNome(c.nome));
  if (clienteEmprestimo) atualizarMateriaisEmprestimo();

  if (!lista.ok) {
    linhaVazia(tbody, 8, mensagemDeErro(lista.data, "Não foi possível carregar os empréstimos."));
    return;
  }
  emprestimos = lista.data;
  renderizarEmprestimos();
}

function renderizarEmprestimos() {
  const tbody = document.getElementById("tabelaEmprestimos");
  const termo = document.getElementById("buscaEmprestimos").value;

  const lista = emprestimos.filter((e) =>
    combinaComBusca([tituloMaterial(e.material_id), nomePorId(clientes, e.cliente_id), e.id], termo));

  if (lista.length === 0) {
    const vazio = { abertos: "Nenhum empréstimo em aberto.", atrasados: "Nenhum empréstimo atrasado.", todos: "Nenhum empréstimo registrado ainda." };
    linhaVazia(tbody, 8, termo.trim() ? `Nada encontrado para "${termo.trim()}".` : vazio[filtroEmprestimos]);
    document.getElementById("contagemEmprestimos").textContent = "";
    return;
  }

  tbody.innerHTML = "";
  const template = document.getElementById("linhaEmprestimoTemplate");

  lista.forEach((emprestimo) => {
    const node = template.content.cloneNode(true);
    const material = materialPorId(emprestimo.material_id);
    node.querySelector(".t-id").textContent = emprestimo.id;
    node.querySelector(".t-material").textContent = tituloMaterial(emprestimo.material_id);
    node.querySelector(".t-tipo").textContent = material ? capitalizar(material.tipo) : "";
    node.querySelector(".t-cliente").textContent = nomePorId(clientes, emprestimo.cliente_id);
    node.querySelector(".t-data").textContent = formatarData(emprestimo.data_emprestimo);
    node.querySelector(".t-prazo").textContent = emprestimo.is_active ? formatarData(prazoDevolucao(emprestimo)) : "—";
    node.querySelector(".t-devolucao").textContent = formatarData(emprestimo.data_devolucao);
    aplicarSelo(node.querySelector(".t-status"), emprestimo.status);

    const botao = node.querySelector(".b-devolver");
    if (emprestimo.is_active) {
      botao.addEventListener("click", () => devolverEmprestimo(emprestimo));
    } else {
      botao.remove();
    }
    tbody.appendChild(node);
  });

  document.getElementById("contagemEmprestimos").textContent = plural(lista.length, "empréstimo", "empréstimos");
}

// ---------- Etapa 1: cliente ----------

function emprestimosAtivosDo(clienteId) {
  return todosEmprestimos.filter((e) => e.is_active && e.cliente_id === clienteId);
}

document.getElementById("formEmpCliente").addEventListener("submit", (e) => {
  e.preventDefault();
  limparInvalidos(e.target);
  if (!exigirSelecao("empCliente", "o cliente")) return;

  const id = parseInt(document.getElementById("empCliente").value, 10);
  const cliente = clientes.find((c) => c.id === id);
  const ativos = emprestimosAtivosDo(id);

  // As mesmas regras do back-end, conferidas antes de enviar
  if (ativos.some((emp) => emp.status === "ATRASADO")) {
    campoInvalido("empCliente", `${cliente.nome} tem um empréstimo atrasado. Registre a devolução antes de emprestar de novo.`);
    return;
  }
  if (ativos.length >= LIMITE_EMPRESTIMOS) {
    campoInvalido("empCliente", `${cliente.nome} já está com ${LIMITE_EMPRESTIMOS} empréstimos ativos, que é o limite.`);
    return;
  }

  ativarEtapaMaterial(cliente, ativos.length);
});

function ativarEtapaMaterial(cliente, quantidadeAtivos) {
  clienteEmprestimo = cliente;
  document.getElementById("chipEmpNome").textContent = cliente.nome;
  document.getElementById("chipEmpInfo").textContent =
    `· ${plural(quantidadeAtivos, "empréstimo ativo", "empréstimos ativos")} de ${LIMITE_EMPRESTIMOS}`;
  document.getElementById("chipEmpCliente").hidden = false;
  document.getElementById("formEmpCliente").hidden = true;
  document.getElementById("fieldsetEmprestimo").disabled = false;
  const passo = document.getElementById("passoEmp1");
  passo.classList.add("feito");
  passo.innerHTML = '<i class="fa-solid fa-check"></i>';
  atualizarMateriaisEmprestimo();
  document.getElementById("empMaterial").focus();
}

function resetarEtapaCliente() {
  clienteEmprestimo = null;
  document.getElementById("formEmpCliente").reset();
  document.getElementById("formEmpCliente").hidden = false;
  document.getElementById("chipEmpCliente").hidden = true;
  document.getElementById("formEmprestimo").reset();
  document.getElementById("fieldsetEmprestimo").disabled = true;
  ["passoEmp1", "passoEmp2"].forEach((id, i) => {
    const passo = document.getElementById(id);
    passo.classList.remove("feito");
    passo.textContent = String(i + 1);
  });
}

document.getElementById("btnTrocarEmpCliente").addEventListener("click", resetarEtapaCliente);

// ---------- Etapa 2: material ----------

// Disponível para todos, ou RESERVADO para este cliente (reserva com o exemplar vinculado)
function materialPodeSerEmprestado(material) {
  if (!material.is_active) return false;
  if (material.status === "DISPONIVEL") return true;
  return material.status === "RESERVADO" && reservasAtivas.some((r) =>
    r.material_id === material.id && r.cliente_id === clienteEmprestimo.id);
}

function atualizarMateriaisEmprestimo() {
  const elegiveis = materiais.filter(materialPodeSerEmprestado);
  preencherSelect("empMaterial", elegiveis, (m) =>
    `${capitalizar(m.titulo)} (${m.tipo}${m.status === "RESERVADO" ? ", reservado para este cliente" : ""})`,
    "Selecione o livro ou a revista");
}

document.getElementById("formEmprestimo").addEventListener("submit", async (e) => {
  e.preventDefault();
  limparInvalidos(e.target);
  if (!clienteEmprestimo) {
    showToast("Escolha o cliente primeiro.", "err");
    return;
  }
  if (!exigirSelecao("empMaterial", "o livro ou a revista")) return;

  const payload = {
    cliente_id: clienteEmprestimo.id,
    material_id: parseInt(document.getElementById("empMaterial").value, 10),
  };

  await comBotaoOcupado(e.target, async () => {
    const { ok, data } = await chamarApi("POST", "/emprestimo", payload);
    if (!ok) {
      showToast(mensagemDeErro(data, "Erro ao registrar o empréstimo."), "err");
      return;
    }
    const passo = document.getElementById("passoEmp2");
    passo.classList.add("feito");
    passo.innerHTML = '<i class="fa-solid fa-check"></i>';
    showToast(`Empréstimo registrado para ${clienteEmprestimo.nome}. Devolver até ${formatarData(prazoDevolucao(data))}.`, "ok");
    setTimeout(resetarEtapaCliente, 1400);
    carregarEmprestimos();
  });
});

// ---------- Devolução ----------

async function devolverEmprestimo(emprestimo) {
  const confirmou = await pedirConfirmacao(
    "Registrar devolução?",
    `"${tituloMaterial(emprestimo.material_id)}", emprestado a ${nomePorId(clientes, emprestimo.cliente_id)} em ${formatarData(emprestimo.data_emprestimo)}. Se houver reserva para este título, o exemplar fica separado para a reserva mais antiga.`,
    "Registrar devolução",
  );
  if (!confirmou) return;

  const { ok, data } = await chamarApi("PATCH", `/emprestimo/${emprestimo.id}/devolver`);
  if (!ok) {
    showToast(mensagemDeErro(data, "Erro ao registrar a devolução."), "err");
    return;
  }
  showToast("Devolução registrada.", "ok");
  carregarEmprestimos();
}

// ---------- Filtros e busca ----------

document.querySelectorAll("[data-filtro-emp]").forEach((aba) => {
  aba.addEventListener("click", () => selecionarFiltroEmprestimos(aba.dataset.filtroEmp));
});

// Só marca a aba (usado também pelo link "Ver todos" do Painel)
function definirFiltroEmprestimos(filtro) {
  filtroEmprestimos = filtro;
  document.querySelectorAll("[data-filtro-emp]").forEach((aba) => {
    aba.setAttribute("aria-selected", String(aba.dataset.filtroEmp === filtro));
  });
}

function selecionarFiltroEmprestimos(filtro) {
  definirFiltroEmprestimos(filtro);
  carregarEmprestimos();
}

document.getElementById("buscaEmprestimos").addEventListener("input", renderizarEmprestimos);
