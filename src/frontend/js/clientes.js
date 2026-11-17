// Tela de Clientes: cadastro, lista, edição, inativação e reativação.

async function carregarClientes() {
  const tbody = document.getElementById("tabelaClientes");
  linhaCarregando(tbody, 5);
  const { ok, data } = await chamarApi("GET", "/cliente");
  if (!ok) {
    linhaVazia(tbody, 5, mensagemDeErro(data, "Não foi possível carregar os clientes."));
    return;
  }
  clientes = data; // a mesma lista usada pelas outras telas
  renderizarClientes();
}

function formatarCpf(cpf) {
  return cpf && cpf.length === 11 ? `${cpf.slice(0, 3)}.${cpf.slice(3, 6)}.${cpf.slice(6, 9)}-${cpf.slice(9)}` : cpf;
}

function formatarTelefone(tel) {
  if (!tel) return "—";
  if (tel.length === 11) return `(${tel.slice(0, 2)}) ${tel.slice(2, 7)}-${tel.slice(7)}`;
  if (tel.length === 10) return `(${tel.slice(0, 2)}) ${tel.slice(2, 6)}-${tel.slice(6)}`;
  return tel;
}

function renderizarClientes() {
  const tbody = document.getElementById("tabelaClientes");
  const termo = document.getElementById("buscaClientes").value;
  const mostrarInativos = document.getElementById("inativosClientes").checked;

  const lista = clientes.filter((c) =>
    (mostrarInativos || c.is_active) &&
    combinaComBusca([c.nome, c.cpf, formatarCpf(c.cpf), c.telefone, c.bairro, c.rua], termo));

  if (lista.length === 0) {
    linhaVazia(tbody, 5, termo.trim() ? `Nenhum cliente encontrado para "${termo.trim()}".` : "Nenhum cliente cadastrado ainda.");
    document.getElementById("contagemClientes").textContent = "";
    return;
  }

  tbody.innerHTML = "";
  const template = document.getElementById("linhaClienteTemplate");

  [...lista].sort((a, b) => a.nome.localeCompare(b.nome, "pt-BR")).forEach((cliente) => {
    const node = template.content.cloneNode(true);
    node.querySelector("tr").classList.toggle("inativa", !cliente.is_active);
    node.querySelector(".t-nome").textContent = cliente.nome;
    node.querySelector(".t-cpf").textContent = `CPF ${formatarCpf(cliente.cpf)}`;
    node.querySelector(".t-telefone").textContent = formatarTelefone(cliente.telefone);
    node.querySelector(".t-endereco").textContent = `${cliente.rua}, ${cliente.numero}`;
    node.querySelector(".t-bairro").textContent = [cliente.complemento, cliente.bairro].filter(Boolean).join(", ");
    aplicarSeloAtivo(node.querySelector(".t-situacao"), cliente.is_active);

    node.querySelector(".b-editar").addEventListener("click", () => abrirEdicaoCliente(cliente));

    const botaoAtivacao = node.querySelector(".b-ativacao");
    if (cliente.is_active) {
      botaoAtivacao.title = "Inativar";
      botaoAtivacao.classList.add("perigo");
      botaoAtivacao.addEventListener("click", () => inativarCliente(cliente));
    } else {
      botaoAtivacao.title = "Reativar";
      botaoAtivacao.innerHTML = '<i class="fa-solid fa-power-off"></i>';
      botaoAtivacao.addEventListener("click", () => ativarCliente(cliente));
    }
    botaoAtivacao.setAttribute("aria-label", botaoAtivacao.title);

    tbody.appendChild(node);
  });

  const ocultos = clientes.length - lista.length;
  document.getElementById("contagemClientes").textContent =
    plural(lista.length, "cliente", "clientes") + (ocultos && !termo.trim() ? ` (${ocultos} inativo(s) oculto(s))` : "");
}

// As mesmas regras da entidade Cliente: nome com 3+ letras, CPF com 11 dígitos, telefone com 10 ou 11
function validarDadosCliente(prefixo, comCpf) {
  if (!exigirTexto(`${prefixo}Nome`, "Nome", 3)) return false;
  if (comCpf && somenteDigitos(document.getElementById(`${prefixo}Cpf`).value).length !== 11) {
    return campoInvalido(`${prefixo}Cpf`, "CPF: informe os 11 dígitos, com ou sem pontuação.");
  }
  const digitosTelefone = somenteDigitos(document.getElementById(`${prefixo}Telefone`).value).length;
  if (digitosTelefone !== 10 && digitosTelefone !== 11) {
    return campoInvalido(`${prefixo}Telefone`, "Telefone: informe DDD + número (10 ou 11 dígitos).");
  }
  if (!exigirTexto(`${prefixo}Rua`, "a rua")) return false;
  if (!exigirInteiroPositivo(`${prefixo}Numero`, "Número")) return false;
  return exigirTexto(`${prefixo}Bairro`, "o bairro");
}

function lerDadosCliente(prefixo) {
  const complemento = document.getElementById(`${prefixo}Complemento`).value.trim();
  return {
    nome: document.getElementById(`${prefixo}Nome`).value.trim(),
    telefone: document.getElementById(`${prefixo}Telefone`).value.trim(),
    rua: document.getElementById(`${prefixo}Rua`).value.trim(),
    numero: parseInt(document.getElementById(`${prefixo}Numero`).value, 10),
    complemento: complemento || null,
    bairro: document.getElementById(`${prefixo}Bairro`).value.trim(),
  };
}

document.getElementById("formCliente").addEventListener("submit", async (e) => {
  e.preventDefault();
  limparInvalidos(e.target);
  if (!validarDadosCliente("cli", true)) return;

  const payload = { ...lerDadosCliente("cli"), cpf: document.getElementById("cliCpf").value.trim() };

  await comBotaoOcupado(e.target, async () => {
    const { ok, data } = await chamarApi("POST", "/cliente", payload);
    if (!ok) {
      showToast(mensagemDeErro(data, "Erro ao cadastrar o cliente."), "err");
      return;
    }
    showToast(`Cliente ${data.nome} cadastrado!`, "ok");
    e.target.reset();
    carregarClientes();
  });
});

function abrirEdicaoCliente(cliente) {
  document.getElementById("editClienteId").value = cliente.id;
  document.getElementById("editClienteCpf").textContent = `CPF ${formatarCpf(cliente.cpf)}`;
  document.getElementById("editClienteNome").value = cliente.nome;
  document.getElementById("editClienteTelefone").value = formatarTelefone(cliente.telefone);
  document.getElementById("editClienteRua").value = cliente.rua;
  document.getElementById("editClienteNumero").value = cliente.numero;
  document.getElementById("editClienteComplemento").value = cliente.complemento || "";
  document.getElementById("editClienteBairro").value = cliente.bairro;
  abrirModal("modalCliente");
}

document.getElementById("formEditarCliente").addEventListener("submit", async (e) => {
  e.preventDefault();
  limparInvalidos(e.target);
  if (!validarDadosCliente("editCliente", false)) return;

  const id = document.getElementById("editClienteId").value;
  const payload = lerDadosCliente("editCliente");

  await comBotaoOcupado(e.target, async () => {
    const { ok, data } = await chamarApi("PATCH", `/cliente/${id}`, payload);
    if (!ok) {
      showToast(mensagemDeErro(data, "Erro ao editar o cliente."), "err");
      return;
    }
    showToast("Cliente atualizado com sucesso!", "ok");
    fecharModal("modalCliente");
    carregarClientes();
  });
});

async function inativarCliente(cliente) {
  const confirmou = await pedirConfirmacao(
    "Inativar cliente?",
    `${cliente.nome} não poderá fazer novos empréstimos nem reservas. Você pode reativar o cadastro depois.`,
    "Inativar cliente",
    true,
  );
  if (!confirmou) return;

  const { ok, data } = await chamarApi("PATCH", `/cliente/${cliente.id}/inativar`);
  if (!ok) {
    showToast(mensagemDeErro(data, "Erro ao inativar o cliente."), "err");
    return;
  }
  showToast("Cliente inativado.", "ok");
  carregarClientes();
}

async function ativarCliente(cliente) {
  const { ok, data } = await chamarApi("PATCH", `/cliente/${cliente.id}/ativar`);
  if (!ok) {
    showToast(mensagemDeErro(data, "Erro ao reativar o cliente."), "err");
    return;
  }
  showToast("Cliente reativado.", "ok");
  carregarClientes();
}

document.getElementById("buscaClientes").addEventListener("input", renderizarClientes);
document.getElementById("inativosClientes").addEventListener("change", renderizarClientes);
