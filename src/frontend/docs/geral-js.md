# `js/geral.js`

## Para que serve

Reúne o que todas as telas usam: o endereço da API, a função que conversa com o back-end, o
aviso na tela, formatação de texto e datas, validação de formulários e as janelas. No projeto
da oficina, essas funções ficam no começo do `script.js` (`const API`, `formatBRL`,
`showToast`). Aqui foram separadas porque são compartilhadas por 9 arquivos.

É o **primeiro** script carregado.

## Constantes e variáveis

| Nome | Linha | O que guarda |
|---|---|---|
| `API` | 3 | Endereço do back-end: `http://localhost:8000` |
| `PRAZO_EMPRESTIMO_DIAS` | 4 | 30 dias, o mesmo prazo de `Emprestimo.verificar_atraso()` |
| `UM_DIA` | 5 | Um dia em milissegundos, para contas com datas |
| `autores`, `editoras`, `categorias`, `clientes`, `materiais` | 8–12 | Listas de apoio, usadas para mostrar nomes no lugar de ids |
| `PALAVRAS_MINUSCULAS` | 96 | "de", "da", "do"... que ficam minúsculas em nomes |
| `ROTULOS_STATUS` | 133 | Texto e cor de cada status que vem da API (`DISPONIVEL` → "Disponível", verde) |

## Funções

### Comunicação com a API

| Função | Linha | O que faz |
|---|---|---|
| `chamarApi(metodo, caminho, corpo)` | 18 | Faz o `fetch` e devolve `{ ok, data }`. Se houver corpo, envia como JSON. Se a API estiver fora do ar, devolve `ok: false` com uma mensagem, em vez de deixar o erro estourar. |
| `mensagemDeErro(data, padrao)` | 35 | Pega o `data.message` que o back-end manda em todo erro (`{ success: false, message: "..." }`) |
| `carregarApoio()` | 39 | Busca autores, editoras, categorias, clientes e materiais ao mesmo tempo, com `Promise.all` |
| `nomePorId(lista, id)` | 54 | Acha o item pelo id e devolve o nome formatado. Se não achar, devolve `#id`. |
| `materialPorId(id)` / `tituloMaterial(id)` | 59 / 63 | Acha o material e devolve o título com a primeira letra maiúscula |

O padrão de uso, igual em todas as telas:

```js
const { ok, data } = await chamarApi("POST", "/livro", payload);
if (!ok) {
  showToast(mensagemDeErro(data, "Erro ao cadastrar o livro."), "err");
  return;
}
```

É o mesmo `if (!resp.ok) { showToast(data.erro, "err"); return; }` da oficina, só com o nome do
campo que o FastAPI do Apolo usa (`message`).

### Aviso e formatação

| Função | Linha | O que faz |
|---|---|---|
| `showToast(mensagem, tipo)` | 70 | Mostra o aviso no canto. `"ok"` (azul) some em 3,2s; `"err"` (vermelho) some em 6s. |
| `esc(valor)` | 85 | Troca `& < > " '` por entidades HTML antes de usar `innerHTML` |
| `capitalizar(texto)` | 89 | Primeira letra maiúscula: "dom casmurro" → "Dom casmurro" |
| `formatarNome(texto)` | 98 | Iniciais maiúsculas, menos "de/da/do/e": "machado de assis" → "Machado de Assis" |
| `normalizar(texto)` | 105 | Tira acentos e deixa minúsculo, para a busca achar "memorias" em "Memórias" |
| `formatarData(valor)` | 109 | Data no formato brasileiro (`11/11/2026`), ou "—" se vier vazia |
| `plural(n, singular, plural)` | 114 | "1 livro" / "2 livros" |
| `prazoDevolucao(emprestimo)` | 118 | Data do empréstimo + 30 dias |
| `diasDesde(data)` | 122 | Quantos dias se passaram desde a data |
| `combinaComBusca(textos, termo)` | 126 | `true` se o termo da busca aparece em algum dos textos |

### Tabelas e selects

| Função | Linha | O que faz |
|---|---|---|
| `aplicarSelo(elemento, status)` | 146 | Escreve o status e pinta o selo com a cor certa |
| `aplicarSeloAtivo(elemento, ativo)` | 152 | Selo "Ativo" (verde) ou "Inativo" (cinza) |
| `linhaVazia(tbody, colunas, texto)` | 158 | Uma linha só, ocupando todas as colunas, com a mensagem |
| `linhaCarregando(tbody, colunas)` | 162 | Linha com o sol girando e "Carregando…" |
| `preencherSelect(id, lista, textoDe, textoVazio)` | 168 | Monta as `<option>` em ordem alfabética e mantém a opção que já estava escolhida |

### Validação

| Função | Linha | O que faz |
|---|---|---|
| `somenteDigitos(texto)` | 181 | "123.456.789-09" → "12345678909" |
| `campoInvalido(id, mensagem)` | 186 | Pinta o campo de vermelho, põe o foco nele, mostra o aviso e devolve `false` |
| `limparInvalidos(form)` | 194 | Tira o vermelho de todos os campos do formulário |
| `exigirTexto(id, rotulo, minimo)` | 198 | Texto obrigatório, com tamanho mínimo |
| `exigirSelecao(id, rotulo)` | 206 | Algum item escolhido no select |
| `exigirAno(id)` | 213 | Ano entre 1 e o ano atual |
| `exigirInteiroPositivo(id, rotulo)` | 222 | Número maior que zero |

Como as funções devolvem `true` ou `false`, a validação é escrita como uma sequência:
`if (!exigirTexto(...)) return false;`. A primeira que falha para o envio.

### Janelas

| Função | Linha | O que faz |
|---|---|---|
| `abrirModal(id)` / `fecharModal(id)` | 232 / 238 | Põe ou tira a classe `show` e coloca o foco no primeiro campo |
| `pedirConfirmacao(titulo, mensagem, textoBotao, perigo)` | 243 | Abre a janela de confirmação e devolve uma `Promise` que vira `true` ou `false` conforme o botão clicado |
| `comBotaoOcupado(form, tarefa)` | 260 | Desativa o botão de enviar enquanto a requisição roda, para não cadastrar em dobro |

## Recursos de JavaScript usados

- `async`/`await` e `fetch`;
- `try/catch` para quando a API não responde (linha 24);
- `Promise.all` para buscar 5 listas em paralelo;
- `new Promise(...)` para esperar o clique na confirmação;
- desestruturação (`const { ok, data } = ...` e `const [a, e, c, cl, m] = ...`);
- template strings com `${...}`;
- parâmetros com valor padrão (`tipo = "ok"`, `minimo = 1`);
- métodos de array: `find`, `filter`, `map`, `some`, `sort`, `join`;
- spread (`[...lista]`), para ordenar sem mexer na lista original;
- expressão regular (`/\D/g` em `somenteDigitos`, `/[&<>"']/g` em `esc`);
- operador `??` (`valor ?? ""`);
- `toLocaleDateString("pt-BR")` para datas.

## Perguntas que podem cair na defesa

**Por que `chamarApi` devolve `{ ok, data }` em vez de lançar erro?**
Para cada tela tratar o erro com um `if` simples, como na oficina, sem precisar de `try/catch`
em todo lugar. O único `try/catch` fica aqui dentro, para o caso de a API estar desligada.

**Para que serve o `esc()`?**
Para impedir que um texto vindo do banco seja interpretado como HTML quando a tela usa
`innerHTML`. Por exemplo, um título `<img onerror=...>` viraria código. Com `textContent` não
precisa, porque ele nunca interpreta HTML.

**Por que validar no front se o back-end já valida?**
Para avisar antes, sem ida ao servidor, e com a mensagem no campo certo. O back-end continua
validando, porque o front pode ser burlado.

**Como a confirmação espera o clique se o código não para?**
`pedirConfirmacao` devolve uma `Promise`. A tela faz `await pedirConfirmacao(...)`, e a função
só continua quando o `onclick` de "Confirmar" ou "Voltar" chama `resolver(true/false)`.
