// Funções usadas por todas as telas: endereço da API, avisos, formatação e listas de apoio.

const API = "http://localhost:8000";
const PRAZO_EMPRESTIMO_DIAS = 30; // o mesmo de Emprestimo.verificar_atraso()
const UM_DIA = 24 * 60 * 60 * 1000;

// Listas usadas para mostrar nomes no lugar de ids (autor_id, cliente_id...)
let autores = [];
let editoras = [];
let categorias = [];
let clientes = [];
let materiais = [];

// ---------- Comunicação com a API ----------

// Faz a requisição e devolve { ok, data }. Se o servidor estiver fora do ar,
// devolve ok = false com uma mensagem, em vez de deixar o erro estourar.
async function chamarApi(metodo, caminho, corpo) {
  const opcoes = { method: metodo, headers: {} };
  if (corpo !== undefined) {
    opcoes.headers["Content-Type"] = "application/json";
    opcoes.body = JSON.stringify(corpo);
  }
  try {
    const resp = await fetch(`${API}${caminho}`, opcoes);
    const texto = await resp.text();
    const data = texto ? JSON.parse(texto) : null;
    return { ok: resp.ok, data };
  } catch (erro) {
    return { ok: false, data: { message: `Não foi possível falar com a API em ${API}. Ela está rodando?` } };
  }
}

// O back-end devolve os erros como { success: false, message: "..." }
function mensagemDeErro(data, padrao) {
  return (data && data.message) || padrao;
}

async function carregarApoio() {
  const [a, e, c, cl, m] = await Promise.all([
    chamarApi("GET", "/autor"),
    chamarApi("GET", "/editora"),
    chamarApi("GET", "/categoria"),
    chamarApi("GET", "/cliente"),
    chamarApi("GET", "/material"),
  ]);
  autores = a.ok ? a.data : [];
  editoras = e.ok ? e.data : [];
  categorias = c.ok ? c.data : [];
  clientes = cl.ok ? cl.data : [];
  materiais = m.ok ? m.data : [];
}

function nomePorId(lista, id) {
  const item = lista.find((i) => i.id === id);
  return item ? formatarNome(item.nome) : `#${id}`;
}

function materialPorId(id) {
  return materiais.find((m) => m.id === id);
}

function tituloMaterial(id) {
  const material = materialPorId(id);
  return material ? capitalizar(material.titulo) : `Material #${id}`;
}

// ---------- Aviso (toast) ----------

function showToast(mensagem, tipo = "ok") {
  const toast = document.getElementById("toast");
  const icone = tipo === "ok" ? "fa-circle-check" : "fa-triangle-exclamation";
  toast.innerHTML = `<i class="fa-solid ${icone}"></i><span></span>`;
  toast.querySelector("span").textContent = mensagem;
  toast.className = `toast show ${tipo}`;
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => {
    toast.className = "toast";
  }, tipo === "ok" ? 3200 : 6000);
}

// ---------- Formatação ----------

// Escapa texto antes de usar em innerHTML
function esc(valor) {
  return String(valor ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function capitalizar(texto) {
  const t = String(texto ?? "");
  return t.charAt(0).toUpperCase() + t.slice(1);
}

// O back-end grava nomes de autor, editora e categoria em minúsculas.
// Aqui eles voltam a ter iniciais maiúsculas só para exibir: "machado de assis" → "Machado de Assis"
const PALAVRAS_MINUSCULAS = ["de", "da", "do", "das", "dos", "e"];

function formatarNome(texto) {
  return String(texto ?? "").split(" ").map((palavra, i) =>
    i > 0 && PALAVRAS_MINUSCULAS.includes(palavra.toLowerCase()) ? palavra.toLowerCase() : capitalizar(palavra),
  ).join(" ");
}

// Tira acentos e deixa em minúsculas, para a busca não depender disso
function normalizar(texto) {
  return String(texto ?? "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
}

function formatarData(valor) {
  if (!valor) return "—";
  return new Date(valor).toLocaleDateString("pt-BR");
}

function plural(n, singular, pluralTexto) {
  return `${n} ${n === 1 ? singular : pluralTexto}`;
}

function prazoDevolucao(emprestimo) {
  return new Date(new Date(emprestimo.data_emprestimo).getTime() + PRAZO_EMPRESTIMO_DIAS * UM_DIA);
}

function diasDesde(data) {
  return Math.floor((Date.now() - new Date(data).getTime()) / UM_DIA);
}

function combinaComBusca(textos, termo) {
  const busca = normalizar(termo.trim());
  return !busca || normalizar(textos.join(" ")).includes(busca);
}

// ---------- Selos de situação ----------

const ROTULOS_STATUS = {
  DISPONIVEL: ["Disponível", "louro"],
  EMPRESTADO: ["Emprestado", "ouro"],
  RESERVADO: ["Reservado", "lapis"],
  ABERTO: ["Aberto", "ouro"],
  ATRASADO: ["Atrasado", "granada"],
  DEVOLVIDO: ["Devolvido", "louro"],
  ABERTA: ["Aberta", "ouro"],
  ATENDIDA: ["Atendida", "louro"],
  CANCELADA: ["Cancelada", "neutro"],
  EXPIRADA: ["Expirada", "neutro"],
};

function aplicarSelo(elemento, status) {
  const [texto, tom] = ROTULOS_STATUS[status] || [status, "neutro"];
  elemento.textContent = texto;
  elemento.className = `selo selo-${tom}`;
}

function aplicarSeloAtivo(elemento, ativo) {
  elemento.textContent = ativo ? "Ativo" : "Inativo";
  elemento.className = `selo ${ativo ? "selo-louro" : "selo-neutro"}`;
}

// Mensagem dentro da tabela quando não há linhas
function linhaVazia(tbody, colunas, texto) {
  tbody.innerHTML = `<tr><td colspan="${colunas}" class="estado"><strong>${esc(texto)}</strong></td></tr>`;
}

function linhaCarregando(tbody, colunas) {
  tbody.innerHTML = `<tr><td colspan="${colunas}" class="estado"><span class="girando"></span>Carregando…</td></tr>`;
}

// ---------- Selects ----------

function preencherSelect(id, lista, textoDe, textoVazio = "Selecione") {
  const select = document.getElementById(id);
  const valorAtual = select.value;
  const ordenada = [...lista].sort((a, b) => textoDe(a).localeCompare(textoDe(b), "pt-BR"));
  select.innerHTML = `<option value="">${esc(lista.length ? textoVazio : "Nada cadastrado ainda")}</option>` +
    ordenada.map((i) => `<option value="${i.id}">${esc(textoDe(i))}</option>`).join("");
  if ([...select.options].some((opt) => opt.value === valorAtual)) {
    select.value = valorAtual;
  }
}

// ---------- Validação dos formulários ----------

function somenteDigitos(texto) {
  return String(texto).replace(/\D/g, "");
}

// Marca o campo em vermelho, mostra o aviso e devolve false para interromper o envio
function campoInvalido(id, mensagem) {
  const campo = document.getElementById(id);
  campo.classList.add("invalido");
  campo.focus();
  showToast(mensagem, "err");
  return false;
}

function limparInvalidos(form) {
  form.querySelectorAll(".invalido").forEach((campo) => campo.classList.remove("invalido"));
}

function exigirTexto(id, rotulo, minimo = 1) {
  const valor = document.getElementById(id).value.trim();
  if (valor.length < minimo) {
    return campoInvalido(id, minimo > 1 ? `${rotulo}: informe pelo menos ${minimo} caracteres.` : `Informe ${rotulo.toLowerCase()}.`);
  }
  return true;
}

function exigirSelecao(id, rotulo) {
  if (!document.getElementById(id).value) {
    return campoInvalido(id, `Escolha ${rotulo}.`);
  }
  return true;
}

function exigirAno(id) {
  const ano = parseInt(document.getElementById(id).value, 10);
  const atual = new Date().getFullYear();
  if (!ano || ano <= 0 || ano > atual) {
    return campoInvalido(id, `Ano de publicação: use um ano entre 1 e ${atual}.`);
  }
  return true;
}

function exigirInteiroPositivo(id, rotulo) {
  const numero = parseInt(document.getElementById(id).value, 10);
  if (!numero || numero <= 0) {
    return campoInvalido(id, `${rotulo}: informe um número maior que zero.`);
  }
  return true;
}

// ---------- Janelas (modais) ----------

function abrirModal(id) {
  document.getElementById(id).classList.add("show");
  const primeiro = document.querySelector(`#${id} input:not([type=hidden]), #${id} select`);
  if (primeiro) primeiro.focus();
}

function fecharModal(id) {
  document.getElementById(id).classList.remove("show");
}

// Pergunta de confirmação. Resolve true se a pessoa confirmar.
function pedirConfirmacao(titulo, mensagem, textoBotao, perigo = false) {
  document.getElementById("confirmarTitulo").textContent = titulo;
  document.getElementById("confirmarMensagem").textContent = mensagem;
  const sim = document.getElementById("btnConfirmarSim");
  const nao = document.getElementById("btnConfirmarNao");
  sim.textContent = textoBotao;
  sim.className = `botao ${perigo ? "botao-perigo" : "botao-primario"}`;
  abrirModal("modalConfirmar");
  sim.focus();

  return new Promise((resolver) => {
    sim.onclick = () => { fecharModal("modalConfirmar"); resolver(true); };
    nao.onclick = () => { fecharModal("modalConfirmar"); resolver(false); };
  });
}

// Desativa o botão enquanto a requisição está em andamento
async function comBotaoOcupado(form, tarefa) {
  const botao = form.querySelector("[type=submit]");
  botao.disabled = true;
  botao.classList.add("carregando");
  try {
    await tarefa();
  } finally {
    botao.disabled = false;
    botao.classList.remove("carregando");
  }
}
