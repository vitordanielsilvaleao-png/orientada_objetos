// Relatórios: números do acervo, ranking de empréstimos, atrasos e gráficos por tipo e categoria.

const LIMITE_RANKING = 10;
const LIMITE_CATEGORIAS = 8;

async function carregarRelatorios() {
  ["relRanking", "relAtrasados", "relTipo", "relCategoria"].forEach((id) => {
    document.getElementById(id).innerHTML = '<p class="estado"><span class="girando"></span>Carregando…</p>';
  });
  await carregarApoio();

  const [total, disponiveis, emprestados, porTipo, porCategoria, todos, atrasados] = await Promise.all([
    chamarApi("GET", "/material/quantidade/total"),
    chamarApi("GET", "/material/quantidade/disponiveis"),
    chamarApi("GET", "/material/emprestados"),
    chamarApi("GET", "/material/quantidade/tipo"),
    chamarApi("GET", "/material/quantidade/categoria"),
    chamarApi("GET", "/emprestimo"),
    chamarApi("GET", "/emprestimo/atrasados"),
  ]);

  desenharNumerosRelatorio(total, disponiveis, emprestados, atrasados);
  desenharRanking(todos);
  desenharAtrasados(atrasados);
  desenharTipos(porTipo);
  desenharCategorias(porCategoria);
}

function desenharNumerosRelatorio(total, disponiveis, emprestados, atrasados) {
  const numeros = [
    { rotulo: "Materiais no acervo", valor: total.ok ? total.data.quantidade : null },
    { rotulo: "Disponíveis", valor: disponiveis.ok ? disponiveis.data.quantidade : null },
    { rotulo: "Emprestados", valor: emprestados.ok ? emprestados.data.length : null },
    { rotulo: "Devoluções atrasadas", valor: atrasados.ok ? atrasados.data.length : null, alerta: true },
  ];
  document.getElementById("relNumeros").innerHTML = numeros.map((n) => `
    <div class="numero ${n.alerta && n.valor ? "numero-alerta" : ""}">
      <span class="numero-valor">${n.valor ?? "—"}</span>
      <span class="numero-rotulo">${esc(n.rotulo)}</span>
    </div>`).join("");
}

// Gráfico de barras horizontais feito só com HTML e CSS
function graficoBarras(itens, ranking = false) {
  const maximo = Math.max(...itens.map((i) => i.valor), 1);
  return `
    <ol class="grafico ${ranking ? "grafico-ranking" : ""}">
      ${itens.map((item, pos) => `
        <li class="grafico-item" title="${esc(item.rotulo)}: ${item.valor}">
          ${ranking ? `<span class="grafico-pos">${pos === 0 ? '<i class="fa-solid fa-crown"></i>' : pos + 1}</span>` : ""}
          <div class="grafico-texto">
            <span class="grafico-rotulo">${esc(item.rotulo)}${item.detalhe ? `<small>${esc(item.detalhe)}</small>` : ""}</span>
            <span class="grafico-valor">${item.valor}</span>
          </div>
          <div class="grafico-trilho"><span class="grafico-barra" style="width: ${((item.valor / maximo) * 100).toFixed(1)}%"></span></div>
        </li>`).join("")}
    </ol>`;
}

function mensagemRelatorio(id, texto, erro = false) {
  document.getElementById(id).innerHTML =
    `<div class="estado ${erro ? "estado-erro" : ""}"><strong>${esc(texto)}</strong></div>`;
}

function desenharRanking(resp) {
  if (!resp.ok) return mensagemRelatorio("relRanking", "Não foi possível carregar os empréstimos.", true);
  if (resp.data.length === 0) return mensagemRelatorio("relRanking", "Nenhum empréstimo registrado ainda.");

  // Conta quantas vezes cada material foi emprestado
  const contagem = new Map();
  resp.data.forEach((e) => contagem.set(e.material_id, (contagem.get(e.material_id) || 0) + 1));

  const itens = [...contagem.entries()]
    .map(([id, valor]) => {
      const material = materialPorId(id);
      return { rotulo: tituloMaterial(id), detalhe: material ? capitalizar(material.tipo) : "", valor };
    })
    .sort((a, b) => b.valor - a.valor || a.rotulo.localeCompare(b.rotulo, "pt-BR"))
    .slice(0, LIMITE_RANKING);

  document.getElementById("relRanking").innerHTML = graficoBarras(itens, true);
}

function desenharAtrasados(resp) {
  if (!resp.ok) return mensagemRelatorio("relAtrasados", "Não foi possível carregar os atrasos.", true);
  if (resp.data.length === 0) return mensagemRelatorio("relAtrasados", "Nenhuma devolução atrasada. Tudo no prazo.");

  const linhas = [...resp.data].sort((a, b) => prazoDevolucao(a) - prazoDevolucao(b));
  document.getElementById("relAtrasados").innerHTML = `
    <div class="tabela-rolagem">
      <table class="tabela">
        <thead><tr><th class="col-principal">Material</th><th>Cliente</th><th>Telefone</th><th>Venceu em</th><th class="col-numero">Dias de atraso</th></tr></thead>
        <tbody>
          ${linhas.map((e) => {
            const cliente = clientes.find((c) => c.id === e.cliente_id);
            return `<tr>
              <td class="col-principal" data-rotulo="Material"><strong>${esc(tituloMaterial(e.material_id))}</strong></td>
              <td data-rotulo="Cliente">${esc(cliente ? cliente.nome : `#${e.cliente_id}`)}</td>
              <td data-rotulo="Telefone">${esc(cliente ? formatarTelefone(cliente.telefone) : "—")}</td>
              <td data-rotulo="Venceu em">${formatarData(prazoDevolucao(e))}</td>
              <td class="col-numero" data-rotulo="Dias de atraso"><span class="atraso">${Math.max(diasDesde(prazoDevolucao(e)), 0)}</span></td>
            </tr>`;
          }).join("")}
        </tbody>
      </table>
    </div>`;
}

function desenharTipos(resp) {
  if (!resp.ok) return mensagemRelatorio("relTipo", "Não foi possível carregar as quantidades por tipo.", true);
  if (resp.data.length === 0) return mensagemRelatorio("relTipo", "Nenhum material cadastrado ainda.");

  const itens = resp.data
    .map((t) => ({ rotulo: capitalizar(t.tipo), valor: t.quantidade }))
    .sort((a, b) => b.valor - a.valor);
  document.getElementById("relTipo").innerHTML = graficoBarras(itens);
}

// Mostra as maiores categorias e junta o resto em "Outras"
function desenharCategorias(resp) {
  if (!resp.ok) return mensagemRelatorio("relCategoria", "Não foi possível carregar as quantidades por categoria.", true);
  if (resp.data.length === 0) return mensagemRelatorio("relCategoria", "Nenhum material cadastrado ainda.");

  const ordenadas = resp.data
    .map((c) => ({ rotulo: nomePorId(categorias, c.categoria_id), valor: c.quantidade }))
    .sort((a, b) => b.valor - a.valor || a.rotulo.localeCompare(b.rotulo, "pt-BR"));
  const itens = ordenadas.slice(0, LIMITE_CATEGORIAS);
  const resto = ordenadas.slice(LIMITE_CATEGORIAS);
  if (resto.length) {
    itens.push({ rotulo: "Outras", detalhe: plural(resto.length, "categoria", "categorias"), valor: resto.reduce((soma, c) => soma + c.valor, 0) });
  }
  document.getElementById("relCategoria").innerHTML = graficoBarras(itens);
}

document.getElementById("btnImprimir").addEventListener("click", () => window.print());
