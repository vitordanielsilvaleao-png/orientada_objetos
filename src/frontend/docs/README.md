# Documentação dos arquivos do front (apolo-front-2)

Um documento por arquivo. Cada um explica para que o arquivo serve, as variáveis e as funções
(com a linha onde ficam), os eventos, as rotas da API usadas, os recursos de JavaScript que
aparecem nele e as perguntas que podem cair na defesa oral, com a resposta.

| Arquivo | Documento | O que faz |
|---|---|---|
| `index.html` | [index-html.md](index-html.md) | Estrutura de todas as telas, templates e janelas |
| `css/style.css` | [style-css.md](style-css.md) | Identidade visual e peças do padrão da oficina |
| `js/geral.js` | [geral-js.md](geral-js.md) | Funções usadas por todas as telas |
| `js/navegacao.js` | [navegacao-js.md](navegacao-js.md) | Menu lateral, troca de telas, janelas e início |
| `js/painel.js` | [painel-js.md](painel-js.md) | Tela inicial com o céu e os números |
| `js/livros.js` | [livros-js.md](livros-js.md) | Cadastro e lista de livros |
| `js/revistas.js` | [revistas-js.md](revistas-js.md) | Cadastro e lista de revistas |
| `js/emprestimos.js` | [emprestimos-js.md](emprestimos-js.md) | Empréstimo em etapas e devolução |
| `js/reservas.js` | [reservas-js.md](reservas-js.md) | Reserva por título, atender e cancelar |
| `js/relatorios.js` | [relatorios-js.md](relatorios-js.md) | Números, ranking e gráficos |
| `js/clientes.js` | [clientes-js.md](clientes-js.md) | Cadastro e lista de clientes |
| `js/catalogo.js` | [catalogo-js.md](catalogo-js.md) | Autores, editoras e categorias |

## Como os arquivos se ligam

```
index.html ── carrega ──> css/style.css
           └─ carrega, nesta ordem ──> geral.js → painel.js → livros.js → revistas.js →
                                        emprestimos.js → reservas.js → relatorios.js →
                                        clientes.js → catalogo.js → navegacao.js
```

- **`geral.js` vem primeiro** porque todos os outros usam as funções dele (`chamarApi`,
  `showToast`, `esc`...).
- **`navegacao.js` vem por último** porque o `SECOES` dele aponta para as funções
  `carregarLivros`, `carregarClientes`... dos outros arquivos, que precisam já existir. É ele
  que dá a partida no sistema, chamando `init()`.
- Os arquivos não usam `import`/`export`. São scripts comuns, que dividem o mesmo escopo global.
  Por isso a ordem das tags `<script>` importa.

## Padrão repetido em todas as telas

Toda tela de cadastro segue o mesmo roteiro, igual ao projeto da oficina do professor:

1. `carregarX()` busca os dados com `chamarApi("GET", ...)` e guarda numa variável `let`;
2. `renderizarX()` filtra pela busca, clona o `<template>` da linha e preenche com `textContent`;
3. o `submit` do formulário valida (`exigirTexto`, `campoInvalido`...), monta o `payload`, chama
   `chamarApi("POST", ...)`, mostra o aviso com `showToast` e chama `carregarX()` de novo;
4. editar abre uma janela (`abrirModal`) já preenchida, e salvar faz um `PATCH`;
5. inativar pede confirmação (`pedirConfirmacao`) e faz um `PATCH .../inativar`.
