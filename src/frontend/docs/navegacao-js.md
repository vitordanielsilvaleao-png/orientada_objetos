# `js/navegacao.js`

## Para que serve

Cuida da paginação pelo menu lateral, mostrando uma tela por vez conforme o `#` do endereço.
Também abre e fecha o menu no celular, liga os botões de fechar das janelas, abre o painel
"Conceitos de POO", verifica se a API está no ar e dá a partida no sistema.

É o **último** script carregado, porque usa as funções `carregar...` de todos os outros.

## Constante

| Nome | Linha | O que guarda |
|---|---|---|
| `SECOES` | 5 | Para cada nome de tela, o título da aba do navegador e a função que carrega aquela tela |

```js
const SECOES = {
  painel: { titulo: "Painel", carregar: carregarPainel },
  livros: { titulo: "Livros", carregar: carregarLivros },
  ...
  autores: { titulo: "Autores", carregar: () => carregarCatalogo("autores") },
};
```

As funções são guardadas como valor, sem os parênteses, para serem chamadas depois. Autores,
editoras e categorias usam uma arrow function porque `carregarCatalogo` precisa receber o tipo.

## Funções

| Função | Linha | O que faz |
|---|---|---|
| `mostrarSecao()` | 18 | Lê o `#` do endereço, esconde todas as seções e mostra a pedida. Marca o item do menu como ativo, troca o título da aba e chama a função de carregar da tela. Se o `#` não existir em `SECOES`, abre o Painel. |
| `alternarMenu(abrir)` | 48 | No celular, abre ou fecha a gaveta do menu e o fundo escuro atrás dela |
| `verificarApi()` | 84 | Faz um `GET /categoria` e muda o indicador do rodapé do menu para "Conectado à API" (verde) ou "API indisponível" (vermelho) |
| `init()` | 94 | Chamada uma vez quando a página abre: verifica a API e mostra a tela do endereço atual |

## Eventos

| Evento | Linha | O que acontece |
|---|---|---|
| `hashchange` na janela | 38 | O `#` mudou (clique no menu ou botão Voltar) e chama `mostrarSecao` |
| `click` no documento | 41 | Se o clique foi num link com `data-filtro-destino` (o "Atrasados" do Painel), marca a aba certa em Empréstimos antes de a tela abrir |
| `click` no ☰ / no fundo escuro | 54–55 | Abre / fecha o menu no celular |
| `click` em `[data-fechar]` | 60 | Fecha a janela cujo id está no atributo |
| `click` no fundo da janela | 65 | Fecha a janela, mas só se o clique foi fora dela (`e.target === fundo`) |
| `keydown` (Esc) | 71 | Fecha o menu e qualquer janela aberta |
| `click` em "Conceitos de POO" | 77 | Abre o painel de conceitos |

## Como a troca de tela funciona, passo a passo

1. O bibliotecário clica em **Livros** no menu (`<a href="#livros">`).
2. O navegador muda o endereço para `...index.html#livros` sem recarregar e dispara `hashchange`.
3. `mostrarSecao()` lê `"livros"` de `window.location.hash`.
4. Percorre todas as `.secao`: só a de id `secao-livros` fica com `hidden = false`.
5. Percorre os `.menu-item`: só o de `data-secao="livros"` ganha a classe `ativo`.
6. Chama `SECOES.livros.carregar()`, ou seja, `carregarLivros()`, que busca os dados na API.

## Recursos de JavaScript usados

- objeto com funções como valores (`SECOES`);
- `window.location.hash` e o evento `hashchange`;
- `querySelectorAll(...).forEach(...)`;
- `classList.toggle(nome, condição)`;
- `dataset` (`item.dataset.secao`, `botao.dataset.fechar`);
- `closest()`, para achar o link clicado mesmo quando o clique foi no texto dentro dele;
- delegação de eventos (um `click` no `document` atende links criados depois pelo Painel);
- função invocada na hora: `(function init() { ... })();`, o mesmo formato do final do `script.js` da oficina.

## Perguntas que podem cair na defesa

**Como o sistema troca de tela sem recarregar a página?**
O menu só muda o `#` do endereço. O evento `hashchange` chama `mostrarSecao`, que esconde as
outras seções e mostra a escolhida.

**Por que o link "Atrasados" do Painel usa delegação no `document`?**
Os números do Painel são criados com `innerHTML` depois que a página abre. Um `addEventListener`
feito antes não alcançaria esses elementos. Ouvindo no `document`, o clique chega até ele de
qualquer jeito (bubbling).

**O que acontece se alguém digitar `#qualquercoisa` no endereço?**
`SECOES["qualquercoisa"]` é `undefined`, então `mostrarSecao` usa `"painel"`.
