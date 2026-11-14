# `js/revistas.js`

## Para que serve

Tela de **Revistas**: cadastra, lista (com busca e inativas), edita, inativa e reativa revistas.
Funciona igual a [livros-js.md](livros-js.md), trocando autor e ISBN por **edição** e **ISSN**.

## Variável

| Nome | Linha | O que guarda |
|---|---|---|
| `revistas` | 3 | As revistas que vieram de `GET /revista` |

## Funções

| Função | Linha | O que faz |
|---|---|---|
| `carregarRevistas()` | 5 | Carrega as listas de apoio, preenche os selects e busca as revistas |
| `preencherSelectsRevista()` | 20 | Preenche editora e categoria, no cadastro e na edição |
| `formatarIssn(issn)` | 28 | O back-end guarda `01041789`, e a tela mostra `0104-1789` |
| `renderizarRevistas()` | 32 | Filtra, clona o template e liga os botões de cada linha |
| `validarFormRevista()` | 86 | Confere título, edição > 0, ISSN com 8 dígitos, ano, editora e categoria |
| `abrirEdicaoRevista(revista)` | 123 | Preenche a janela de edição. Recusa revista inativa. |
| `inativarRevista(revista)` / `ativarRevista(revista)` | 166 / 184 | `PATCH /revista/{id}/inativar` / `ativar` |

## Eventos

| Evento | Linha | O que acontece |
|---|---|---|
| `submit` em `#formRevista` | 98 | `POST /revista` |
| `submit` em `#formEditarRevista` | 138 | `PATCH /revista/{id}` |
| `input` na busca / `change` em "Mostrar inativas" | 194–195 | Redesenha a tabela |

## Rotas da API

| Rota | Back-end chamado |
|---|---|
| `GET /revista` | `RevistaService.visualizar()` |
| `POST /revista` | `RevistaService.cadastrar()`, que cria `Revista(...)` |
| `PATCH /revista/{id}` | `Revista.atualizar()`, que sobrescreve o de `Material` e cuida da edição |
| `PATCH /revista/{id}/inativar` / `ativar` | `Material.inativar()` / `ativar()` |

## Reaproveitamento do template de livro

A tabela de revistas tem as mesmas 8 colunas da de livros. Por isso a linha usa o
`linhaLivroTemplate`, trocando o conteúdo da 2ª coluna:

```js
node.querySelector(".t-detalhe").textContent = `Edição ${revista.edicao}`;
node.querySelector(".t-autor").textContent = formatarIssn(revista.issn);  // a coluna "Autor" vira "ISSN"
node.querySelector(".t-autor").dataset.rotulo = "ISSN";                    // rótulo no celular
```

## Regras conferidas antes de enviar

| Regra no front | Regra no back-end |
|---|---|
| ISSN com 8 dígitos (aceita `-`) | `Revista.normalizar_issn()` + `_validar_issn()` |
| Edição maior que zero | `@validates("edicao")` → `_validar_edicao()` |
| Ano entre 1 e o ano atual | `Material._validar_ano_publi()` |

## Perguntas que podem cair na defesa

**Qual a diferença entre Livro e Revista no código?**
As duas herdam de `Material`. Livro acrescenta `isbn` e `autor_id`. Revista acrescenta `issn` e
`edicao`. Na tela, isso aparece como campos diferentes no formulário.

**Por que formatar o ISSN só na tela?**
O banco guarda só os dígitos, para comparar e validar com facilidade. O hífen é só para leitura.
