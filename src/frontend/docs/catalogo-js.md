# `js/catalogo.js`

## Para que serve

Atende **três telas com um código só**: Autores, Editoras e Categorias. As três têm um campo
(Nome), uma tabela com a quantidade de títulos no acervo e a opção de renomear. O que muda entre
elas (rota, ids dos elementos, textos) fica num objeto de configuração, o `CATALOGO`.

## Constante e variáveis

| Nome | Linha | O que guarda |
|---|---|---|
| `CATALOGO` | 4 | A configuração de cada tipo: rota da API, nome no singular e no plural, campo que liga ao material e ids do formulário, da tabela, da busca e da contagem |
| `itensCatalogo` | 19 | `{ autores: [...], editoras: [...], categorias: [...] }` com o que veio da API |
| `livrosDoCatalogo` | 20 | Livros, usados para contar os títulos de cada autor |

```js
autores: {
  rota: "/autor", singular: "autor", plural: "autores", campoMaterial: "autor_id",
  form: "formAutor", campoNome: "autorNome", tabela: "tabelaAutores", ...
},
```

## Funções

| Função | Linha | O que faz |
|---|---|---|
| `carregarCatalogo(tipo)` | 22 | Busca a lista do tipo. Para autores, busca também `/livro`. |
| `contarTitulos(tipo, id)` | 42 | Quantos materiais apontam para aquele autor, editora ou categoria |
| `renderizarCatalogo(tipo)` | 48 | Filtra pela busca, ordena por nome e desenha as linhas |
| `abrirRenomear(tipo, item)` | 77 | Abre a janela `modalNome`, guardando o tipo e o id em campos escondidos |

## Eventos

| Evento | Linha | O que acontece |
|---|---|---|
| `submit` nos 3 formulários de cadastro | 89 | Valida, confere nome repetido e envia `POST` para a rota do tipo |
| `input` nas 3 buscas | 113 | Redesenha a tabela daquele tipo |
| `submit` em `#formEditarNome` | 116 | Lê o tipo do campo escondido e envia `PATCH {rota}/{id}` |

Os eventos de cadastro e busca são ligados num laço:

```js
Object.keys(CATALOGO).forEach((tipo) => {
  const config = CATALOGO[tipo];
  document.getElementById(config.form).addEventListener("submit", ...);
  document.getElementById(config.busca).addEventListener("input", () => renderizarCatalogo(tipo));
});
```

## Por que autores contam pelos livros

`GET /material` devolve livros e revistas, mas sem `autor_id`, que só existe em `Livro`. Para
editoras e categorias basta a lista de materiais. Para autores, o arquivo busca `/livro`.

## Nomes em minúsculas

O back-end grava os nomes normalizados ("machado de assis"). A tela mostra com
`formatarNome()` ("Machado de Assis"), e a conferência de nome repetido compara em minúsculas,
do mesmo jeito que o back-end.

## Rotas da API

| Rota | Back-end chamado |
|---|---|
| `GET /autor`, `/editora`, `/categoria` | `visualizar()` de cada service |
| `POST` nas mesmas rotas | `cadastrar()`: responde 409 se o nome já existe |
| `PATCH /autor/{id}` (e as outras) | `atualizar()` |
| `GET /livro`, `GET /material` | Contar os títulos |

## Recursos de JavaScript usados

- objeto de configuração (dados no lugar de código repetido);
- `Object.keys(...).forEach(...)`;
- acesso dinâmico a propriedade (`CATALOGO[tipo]`, `m[config.campoMaterial]`);
- `Promise.resolve(...)` para manter o `Promise.all` com 2 itens mesmo quando não precisa buscar livros;
- `<input type="hidden">` para a janela de renomear saber de qual tipo é o item.

## Perguntas que podem cair na defesa

**Como um código só atende três telas?**
Tudo o que muda fica no `CATALOGO`. As funções recebem o `tipo` e leem dali a rota e os ids. Se
surgir uma quarta tela parecida, basta acrescentar uma entrada no objeto e a seção no HTML.

**Isso tem relação com POO?**
Tem uma ideia parecida com o `BaseService`: os três services de catálogo seguem o mesmo contrato
(`cadastrar`, `visualizar`, `atualizar`), e o front aproveita isso para tratar os três do mesmo
jeito.

**Por que conferir nome repetido no front se o back-end já devolve 409?**
Para avisar no campo, antes de enviar. Se a lista estiver desatualizada, o 409 do back-end
continua valendo e a mensagem dele aparece no aviso.
