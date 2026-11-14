# `css/style.css`

## Para que serve

Define a aparência do sistema. O arquivo tem duas partes:

1. **Linhas 1–927:** a identidade visual do Apolo, copiada do front antigo (`src/apolo-front/`).
   Ela inclui cores, fontes, menu lateral, botões, tabelas, selos, céu do painel, gráficos e
   avisos.
2. **Linhas 929 em diante:** as peças novas, que seguem o padrão do projeto da oficina: balões "?",
   dicas, etapas numeradas, janelas com `.show`, painel de conceitos e o layout formulário +
   tabela.

## Identidade visual: "a luz de Delfos"

As cores ficam em variáveis no `:root` (linha 7) e são usadas no arquivo todo com `var(--nome)`:

| Variável | Cor | Uso |
|---|---|---|
| `--lapis` | `#13203B` | Azul lápis-lazúli: menu lateral, títulos, botões escuros |
| `--ouro` | `#D6A93A` | Ouro de Apolo: botão principal, destaques, borda dos painéis |
| `--marmore` | `#ECEEF2` | Fundo das páginas, com veios de mármore em SVG (`--veios`) |
| `--louro` | `#3F6233` | Verde-louro: "Disponível", "Ativo", etapa concluída |
| `--granada` | `#962A3A` | Vermelho: erros, "Atrasado", botões de perigo |

Fontes: **Marcellus** nos títulos (lembra inscrição grega) e **Commissioner** no texto.

## Seções do arquivo

| Linhas | Seção |
|---|---|
| 79–100 | Estrutura: grade com menu (264px) + conteúdo |
| 102–223 | Menu lateral, marca, item ativo com a barrinha dourada |
| 225–254 | Cabeçalho das telas, com o ornamento dourado |
| 256–317 | Botões (`botao-primario`, `botao-secundario`, `botao-perigo`, `botao-icone`) |
| 319–477 | Tabelas, busca, abas, chave "Mostrar inativos", estado vazio |
| 490–507 | Selos de situação (`selo-louro`, `selo-ouro`, `selo-granada`...) |
| 509–642 | Painel: céu, sol, lua, estrelas, números, listas |
| 644–703 | Relatórios e gráficos de barras |
| 705–787 | Campos de formulário e janelas |
| 789–821 | Aviso (toast) |
| 823–927 | Responsivo (1100px, 900px, 700px), impressão e movimento reduzido |
| 937–962 | Ícones do Font Awesome no menu e nos botões |
| 968–1011 | `layout-modulo` (formulário + tabela) e `painel-form` |
| 1013–1041 | Etapas numeradas (`.passo`, `.passo.feito`) e o `.chip` do cliente escolhido |
| 1043–1101 | Balão `.poo-info` e dica `.poo-hint` |
| 1103–1118 | Aviso único `#toast` com `.show`, igual ao da oficina |
| 1120–1148 | Janelas `.sobreposicao` / `.janela` |
| 1150–1186 | Painel "Conceitos de POO" |
| 1188–1220 | Céu (sol × lua), largura da página, responsivo novo e impressão |

## Técnicas que vale saber explicar

**Variáveis CSS (`--lapis`, `var(--lapis)`).** Se a cor mudar, ela muda num lugar só.

**Grid.** O `.app` divide a tela em menu + conteúdo com `grid-template-columns: var(--largura-barra) 1fr`.
O `.layout-modulo` divide o conteúdo em formulário (até 340px) + tabela.

**Balão sem JavaScript.** O `.poo-info::after` usa `content: attr(data-tip)` para ler o texto do
HTML. Ele começa com `opacity: 0` e aparece em `:hover` ou `:focus-visible`. O
`white-space: pre-line` respeita as quebras de linha do `&#10;`.

**Classe `show`.** Janelas e aviso ficam escondidos com `opacity: 0; visibility: hidden`. O JS
só adiciona ou remove `show`, e a `transition` faz a animação.

**Responsivo.**
- Até 1699px, o formulário vai para cima da tabela, e os campos se espalham em colunas com
  `repeat(auto-fill, minmax(220px, 1fr))`.
- Até 900px, o menu vira gaveta: `transform: translateX(-100%)` esconde, e a classe `.aberta`
  mostra.
- Até 700px, cada linha da tabela vira um cartão, e o nome da coluna aparece via
  `td::before { content: attr(data-rotulo) }`.

**`display: contents`.** No modo empilhado, `.linha-dupla` e `fieldset` "somem" da grade, e os
campos de dentro passam a ser colunas da grade do formulário.

**Acessibilidade.**
- `:focus-visible` desenha um contorno dourado em quem usa teclado.
- `prefers-reduced-motion` desliga as animações para quem pediu isso no sistema.

**Impressão.** O `@media print` esconde menu, avisos e janelas. É o que deixa o botão
"Imprimir" dos Relatórios sair limpo.

## Perguntas que podem cair na defesa

**Como o site se adapta ao celular?**
Com `@media (max-width: ...)`: o menu vira uma gaveta aberta pelo botão ☰, e as tabelas viram
cartões.

**Como o balão "?" aparece sem JavaScript?**
O pseudo-elemento `::after` pega o texto de `data-tip` com `attr()` e fica invisível. No
`:hover`, a opacidade vai a 1.

**Qual a diferença entre `hidden` e a classe `show`?**
`hidden` (atributo HTML) tira o elemento da tela de vez: é usado nas seções. A classe `show`
é usada nas janelas e no aviso, porque com ela dá para animar a entrada com `transition`.
