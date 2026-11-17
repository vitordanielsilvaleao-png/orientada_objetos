// Painel inicial: céu com o sol (ou a lua) conforme a hora, números do acervo e listas de atenção.

function desenharCeu() {
  const agora = new Date();
  const hora = agora.getHours() + agora.getMinutes() / 60;
  const dia = hora >= 6 && hora < 18;
  const saudacao = hora < 5 ? "Boa noite" : hora < 12 ? "Bom dia" : hora < 18 ? "Boa tarde" : "Boa noite";

  document.getElementById("ceu").className = `ceu ${dia ? "ceu-dia" : "ceu-noite"}`;
  document.getElementById("ceuSaudacao").textContent = `${saudacao}.`;
  document.getElementById("ceuData").textContent =
    capitalizar(agora.toLocaleDateString("pt-BR", { weekday: "long", day: "numeric", month: "long" }));

  // O astro anda pelo arco: 0 = nascente, 1 = poente
  const t = dia ? (hora - 6) / 12 : ((hora - 18 + 24) % 24) / 12;
  const p = Math.min(Math.max(t, 0.04), 0.96);
  const angulo = Math.PI * (1 - p);
  const x = 300 + 260 * Math.cos(angulo);
  const y = 210 - 170 * Math.sin(angulo);
  document.getElementById("astro").setAttribute("transform", `translate(${x.toFixed(1)} ${y.toFixed(1)})`);
}

async function carregarPainel() {
  desenharCeu();
  await carregarApoio();

  const [livrosResp, revistasResp, abertosResp, atrasadosResp, reservasResp] = await Promise.all([
    chamarApi("GET", "/livro"),
    chamarApi("GET", "/revista"),
    chamarApi("GET", "/emprestimo/abertos"),
    chamarApi("GET", "/emprestimo/atrasados"),
    chamarApi("GET", "/reserva/abertas"),
  ]);

  const contarAtivos = (resp) => (resp.ok ? resp.data.filter((i) => i.is_active).length : null);
  const tamanho = (resp) => (resp.ok ? resp.data.length : null);
  const atrasados = atrasadosResp.ok ? atrasadosResp.data : null;
  const reservasAbertas = reservasResp.ok ? reservasResp.data : null;

  // Resumo em uma frase
  const resumo = document.getElementById("ceuResumo");
  if (!abertosResp.ok && !atrasadosResp.ok) {
    resumo.textContent = "Não foi possível consultar a API. Verifique se ela está rodando e recarregue a página.";
  } else {
    const nAbertos = tamanho(abertosResp) || 0;
    const nAtrasados = atrasados ? atrasados.length : 0;
    const nReservas = reservasAbertas ? reservasAbertas.length : 0;
    const partes = [];
    if (nAtrasados) partes.push(plural(nAtrasados, "empréstimo está atrasado", "empréstimos estão atrasados"));
    partes.push(nAbertos ? `${plural(nAbertos, "empréstimo segue", "empréstimos seguem")} em aberto` : "não há empréstimos em aberto");
    if (nReservas) partes.push(`${plural(nReservas, "reserva aguarda", "reservas aguardam")} atendimento`);
    const frase = partes.length > 1 ? `${partes.slice(0, -1).join(", ")} e ${partes[partes.length - 1]}` : partes[0];
    resumo.textContent = `${capitalizar(frase)}.${nAtrasados ? "" : " Nenhum atraso por aqui."}`;
  }

  // Números
  const numeros = [
    { rotulo: "Livros ativos", valor: contarAtivos(livrosResp), destino: "#livros" },
    { rotulo: "Revistas ativas", valor: contarAtivos(revistasResp), destino: "#revistas" },
    { rotulo: "Clientes ativos", valor: clientes.filter((c) => c.is_active).length, destino: "#clientes" },
    { rotulo: "Empréstimos em aberto", valor: tamanho(abertosResp), destino: "#emprestimos" },
    { rotulo: "Atrasados", valor: atrasados ? atrasados.length : null, destino: "#emprestimos", alerta: true, filtro: "atrasados" },
    { rotulo: "Reservas abertas", valor: reservasAbertas ? reservasAbertas.length : null, destino: "#reservas" },
  ];
  document.getElementById("painelNumeros").innerHTML = numeros.map((n) => `
    <a class="numero ${n.alerta && n.valor ? "numero-alerta" : ""}" href="${n.destino}" ${n.filtro ? `data-filtro-destino="${n.filtro}"` : ""}>
      <span class="numero-valor">${n.valor ?? "—"}</span>
      <span class="numero-rotulo">${esc(n.rotulo)}</span>
    </a>`).join("");

  // Listas
  preencherListaPainel("listaAtrasados", atrasados, "Nenhum empréstimo atrasado. Tudo devolvido no prazo.",
    (e) => ({ titulo: tituloMaterial(e.material_id), cliente: nomePorId(clientes, e.cliente_id), meta: `venceu em ${formatarData(prazoDevolucao(e))}` }));
  preencherListaPainel("listaReservas", reservasAbertas, "Nenhuma reserva aguardando atendimento.",
    (r) => ({ titulo: capitalizar(r.titulo), cliente: nomePorId(clientes, r.cliente_id), meta: `desde ${formatarData(r.data)}` }));
}

function preencherListaPainel(id, lista, textoVazio, extrair) {
  const ul = document.getElementById(id);
  if (!lista) {
    ul.innerHTML = '<li class="estado">Não foi possível carregar.</li>';
    return;
  }
  if (lista.length === 0) {
    ul.innerHTML = `<li class="estado">${esc(textoVazio)}</li>`;
    return;
  }
  ul.innerHTML = lista.slice(0, 6).map((item) => {
    const { titulo, cliente, meta } = extrair(item);
    return `<li><div><strong>${esc(titulo)}</strong><small>${esc(cliente)}</small></div><span class="lista-meta">${esc(meta)}</span></li>`;
  }).join("");
}
