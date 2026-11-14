# `index.html`

## Para que serve

É a única página do sistema. Todo o HTML das 10 telas já está escrito aqui. O JavaScript não
cria telas: ele só mostra a seção escolhida no menu, preenche tabelas e selects e reage aos
cliques. Esse é o padrão do projeto da oficina do professor, em que o `index.html` tem os
formulários, os modais e o `<template>` do card.

## Partes do arquivo

| Linhas | Parte | O que tem |
|---|---|---|
| 1–14 | `<head>` | Fontes Commissioner e Marcellus (Google Fonts), ícones do Font Awesome 6.5.1 e o `css/style.css` |
| 17–73 | Menu lateral (`<aside class="barra">`) | Marca com o sol, links `href="#livros"`... com `data-secao`, botão "Conceitos de POO", indicador da API |
| 75–81 | Topo do celular | Botão ☰ que abre o menu em telas pequenas |
| 83–121 | Seção Painel | Céu em SVG com sol e lua (o JS escolhe qual aparece), números e duas listas |
| 123–192 | Seção Livros | Formulário de cadastro à esquerda, tabela à direita |
| 194–261 | Seção Revistas | Mesmo formato de Livros, com edição e ISSN |
| 263–326 | Seção Empréstimos | Etapa 1 (cliente) e etapa 2 (material), abas de filtro e tabela |
| 328–376 | Seção Reservas | Formulário com `<datalist>` de títulos, abas e tabela |
| 378–410 | Seção Relatórios | Números, ranking, atrasos e gráficos (o JS preenche os `div` vazios) |
| 412–481 | Seção Clientes | Formulário com CPF e endereço, tabela |
| 483–570 | Autores, Editoras, Categorias | Três seções iguais, só com um campo Nome |
| 572–640 | `<template>` das linhas | Uma linha de tabela pronta para cada tipo de registro |
| 642–745 | Janelas de edição e confirmação | `modalLivro`, `modalRevista`, `modalCliente`, `modalNome`, `modalConfirmar` |
| 747–843 | Janela "Conceitos de POO" | Classes do back-end, conceitos de POO e tabela tela → rota → método |
| 845–854 | Scripts | Os 10 arquivos JS, em ordem |

## Como as seções funcionam

Cada tela é um `<section id="secao-NOME" class="secao" hidden>`. O atributo `hidden` esconde
todas. O `navegacao.js` lê o endereço (`#livros`) e tira o `hidden` só de `secao-livros`.

Os links do menu são âncoras comuns:

```html
<a href="#livros" class="menu-item" data-secao="livros">...</a>
```

Clicar muda o `#` do endereço, o navegador dispara o evento `hashchange` e a tela troca. Não é
preciso recarregar a página, e o botão "Voltar" do navegador também funciona.

## Templates

```html
<template id="linhaLivroTemplate">
  <tr>
    <td class="col-principal"><strong class="t-titulo"></strong><small class="t-detalhe"></small></td>
    ...
  </tr>
</template>
```

O conteúdo de um `<template>` não aparece na tela. O JavaScript faz uma cópia com
`template.content.cloneNode(true)`, preenche as classes `t-...` com `textContent` e coloca a
cópia na tabela. A mesma ideia está no `ordemCardTemplate` da oficina. O template de livro também
serve para revista, porque as colunas são as mesmas.

## Balões "?" e dicas

```html
<button type="button" class="poo-info" data-tip="Atributo EXCLUSIVO da subclasse Livro&#10;&#10;...">?</button>
```

O texto fica no atributo `data-tip`, e o CSS o mostra num balão ao passar o mouse (`::after` com
`content: attr(data-tip)`). `&#10;` é a quebra de linha dentro do atributo. Os parágrafos
`<p class="poo-hint">` abaixo dos formulários dizem qual método do back-end aquele formulário
aciona.

## Janelas (modais)

As janelas são `<div class="sobreposicao">` que ficam invisíveis até ganharem a classe `show`,
o mesmo esquema do `modal-overlay` da oficina. Os botões de fechar têm
`data-fechar="idDaJanela"`, e o `navegacao.js` liga todos eles de uma vez.

## Formulários

- Todos têm `novalidate`. A validação é feita no JavaScript, com mensagens próprias, e o campo
  errado fica vermelho.
- `required`, `min` e `maxlength` continuam no HTML como documentação e como limite de digitação.
- O formulário da etapa 2 do empréstimo fica dentro de um `<fieldset disabled>`. Com isso, todos
  os campos ficam bloqueados até a etapa 1 terminar.

## Perguntas que podem cair na defesa

**Por que o HTML não é gerado pelo JavaScript, como no front antigo?**
Para seguir o padrão do professor: a estrutura fica visível no HTML, e o JS só cuida do
comportamento. Fica mais fácil achar onde está cada campo.

**O que acontece se um `<script>` for carregado antes do `geral.js`?**
As funções `chamarApi`, `showToast` e as outras ainda não existiriam, e o arquivo daria erro ao
usá-las. Por isso a ordem das tags importa.

**Para que serve o `data-` nos atributos (`data-secao`, `data-tip`, `data-fechar`)?**
São atributos próprios, que guardam informação no HTML. No JS, eles aparecem em
`elemento.dataset`: por exemplo, `botao.dataset.fechar`.

**Por que `<template>` e não `innerHTML` com o texto da linha?**
Com o template, os dados entram por `textContent`, que nunca interpreta HTML. Um título com `<`
ou `"` não quebra a página nem injeta código.
