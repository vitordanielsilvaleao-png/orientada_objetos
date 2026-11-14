# `js/painel.js`

## Para que serve

Tela inicial. Mostra o céu de Apolo com o sol (de dia) ou a lua (à noite) andando pelo arco
conforme a hora, uma frase-resumo da circulação, seis números do acervo e duas listas de
atenção: empréstimos atrasados e reservas aguardando.

## Funções

| Função | Linha | O que faz |
|---|---|---|
| `desenharCeu()` | 3 | Calcula a hora, escolhe dia ou noite, escreve a saudação ("Bom dia", "Boa tarde"...) e a data, e posiciona o astro no arco |
| `carregarPainel()` | 23 | Busca 5 rotas ao mesmo tempo, monta a frase-resumo, os números e as duas listas |
| `preencherListaPainel(id, lista, textoVazio, extrair)` | 78 | Preenche uma lista do painel com até 6 itens. Recebe uma função `extrair` que diz qual título, cliente e data mostrar. |

## Rotas da API

| Rota | Para quê |
|---|---|
| `GET /livro`, `GET /revista` | Contar os ativos |
| `GET /emprestimo/abertos` | Número de empréstimos em aberto |
| `GET /emprestimo/atrasados` | Número e lista de atrasados |
| `GET /reserva/abertas` | Número e lista de reservas aguardando |

Além delas, `carregarApoio()` traz clientes e materiais, para mostrar nomes em vez de ids.

## Detalhes que valem a explicação

**O sol andando no arco.** A hora vira um número de 0 (nascente) a 1 (poente). Com seno e
cosseno, esse número vira um ponto do arco desenhado no SVG:

```js
const angulo = Math.PI * (1 - p);
const x = 300 + 260 * Math.cos(angulo);
const y = 210 - 170 * Math.sin(angulo);
document.getElementById("astro").setAttribute("transform", `translate(${x} ${y})`);
```

O sol e a lua já estão no `index.html`. O CSS esconde um ou outro conforme a classe
`ceu-dia` / `ceu-noite`, que o JS coloca na `<section>`.

**A frase-resumo.** As partes vão para um array (`partes.push(...)`) e depois são juntadas com
vírgula e "e" antes da última: "1 empréstimo segue em aberto e 1 reserva aguarda atendimento."

**Atrasados vêm do agendador.** A lista de atrasados não é calculada aqui. Ela vem de
`/emprestimo/atrasados`, que devolve os empréstimos marcados como ATRASADO pelo agendador do
back-end, que roda de hora em hora (`marcar_atrasado()`).

**Número com link.** Cada número é um `<a>` que leva à tela correspondente. O de "Atrasados" tem
`data-filtro-destino="atrasados"`, para Empréstimos já abrir na aba certa.

## Recursos de JavaScript usados

- `new Date()`, `getHours()`, `toLocaleDateString` com `weekday` e `month: "long"`;
- operador ternário encadeado para a saudação;
- `Math.cos`, `Math.sin`, `Math.min`, `Math.max`;
- `Promise.all` com desestruturação de 5 respostas;
- função passada como parâmetro (`extrair`), um *callback*;
- `slice(0, 6)` para limitar a lista;
- `??` para mostrar "—" quando um número não pôde ser carregado.

## Perguntas que podem cair na defesa

**Por que usar `Promise.all` em vez de 5 `await` seguidos?**
Com `Promise.all`, as 5 requisições saem juntas e a tela espera só a mais lenta. Com 5 `await`
seguidos, cada uma esperaria a anterior terminar.

**De onde vem o "Clientes ativos" se não há `fetch` de clientes aqui?**
Do `carregarApoio()` do `geral.js`, que já preencheu a lista `clientes`. O painel só filtra com
`clientes.filter((c) => c.is_active).length`.
