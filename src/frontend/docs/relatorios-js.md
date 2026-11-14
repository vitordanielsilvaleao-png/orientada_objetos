# `js/relatorios.js`

## Para que serve

Tela de **Relatórios**: quatro números do acervo, o ranking dos materiais mais emprestados, a
tabela de devoluções atrasadas e dois gráficos de barras (acervo por tipo e por categoria). Tem
um botão **Imprimir**.

## Constantes

| Nome | Linha | O que guarda |
|---|---|---|
| `LIMITE_RANKING` | 3 | Mostra no máximo 10 materiais no ranking |
| `LIMITE_CATEGORIAS` | 4 | Mostra 8 categorias; o resto vira "Outras" |

## Funções

| Função | Linha | O que faz |
|---|---|---|
| `carregarRelatorios()` | 6 | Busca 7 rotas ao mesmo tempo e chama cada função de desenho |
| `desenharNumerosRelatorio(...)` | 29 | Materiais no acervo, disponíveis, emprestados e atrasados |
| `graficoBarras(itens, ranking)` | 44 | Gera o HTML de um gráfico de barras horizontais. No ranking, numera as posições e põe uma coroa no 1º lugar. |
| `mensagemRelatorio(id, texto, erro)` | 60 | Mensagem de "vazio" ou de erro dentro de um bloco |
| `desenharRanking(resp)` | 65 | Conta os empréstimos de cada material com um `Map`, ordena e desenha |
| `desenharAtrasados(resp)` | 84 | Tabela com material, cliente, telefone, data de vencimento e dias de atraso |
| `desenharTipos(resp)` | 109 | Gráfico Livro × Revista |
| `desenharCategorias(resp)` | 120 | Gráfico por categoria, juntando as menores em "Outras" |

Evento: `click` em **Imprimir** (linha 135) chama `window.print()`. O CSS de impressão esconde
o menu.

## Rotas da API

| Rota | Back-end chamado |
|---|---|
| `GET /material/quantidade/total` | `MaterialService.contar_quantidade_total()` |
| `GET /material/quantidade/disponiveis` | `MaterialService.contar_quantidade_disponivel()` |
| `GET /material/emprestados` | `MaterialService.consultar_materiais_emprestados()` |
| `GET /material/quantidade/tipo` | `MaterialService.contar_materiais_por_tipo()`, com `func.count` + `group_by` |
| `GET /material/quantidade/categoria` | `MaterialService.contar_materiais_por_categoria()` |
| `GET /emprestimo` | Todos os empréstimos, para o ranking |
| `GET /emprestimo/atrasados` | Os atrasados, para a tabela |

## O ranking, passo a passo

```js
const contagem = new Map();
resp.data.forEach((e) => contagem.set(e.material_id, (contagem.get(e.material_id) || 0) + 1));
```

1. Para cada empréstimo, soma 1 no contador daquele `material_id`.
2. `[...contagem.entries()]` transforma o `Map` em lista de pares `[id, quantidade]`.
3. `map` troca cada par por `{ rotulo, detalhe, valor }`.
4. `sort` ordena do maior para o menor; no empate, por ordem alfabética.
5. `slice(0, 10)` fica com os 10 primeiros.

## O gráfico de barras

Não usa biblioteca: é uma lista `<ol>` em que cada barra é um `<span>` com a largura em
porcentagem do maior valor.

```js
style="width: ${((item.valor / maximo) * 100).toFixed(1)}%"
```

## Recursos de JavaScript usados

- `Map` (`set`, `get`, `entries`);
- `reduce` para somar as categorias de "Outras";
- `Math.max(...lista)` com spread;
- `sort` com dois critérios (`b.valor - a.valor || a.rotulo.localeCompare(...)`);
- `localeCompare(..., "pt-BR")` para ordenar com acentos certos;
- `toFixed(1)` para a porcentagem;
- `return` antecipado (`if (!resp.ok) return mensagemRelatorio(...)`);
- `window.print()`.

## Perguntas que podem cair na defesa

**Quem faz as contas: o front ou o back-end?**
As contagens do acervo (total, por tipo, por categoria) são feitas no banco pelo `MaterialService`,
com `func.count()` e `group_by()`. O ranking de empréstimos é montado no front, contando a lista
de empréstimos.

**Por que usar `Map` e não um objeto `{}`?**
Os dois funcionam. O `Map` guarda a chave como número (o `material_id`) e tem `entries()` para
virar lista e ordenar.

**Como funcionam os dias de atraso?**
`diasDesde(prazoDevolucao(e))` conta os dias desde a data de vencimento (empréstimo + 30 dias).
`Math.max(..., 0)` evita número negativo.
