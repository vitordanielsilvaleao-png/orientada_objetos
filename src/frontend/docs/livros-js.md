# `js/livros.js`

## Para que serve

Tela de **Livros**: cadastra livros, lista os que existem (com busca e opção de mostrar
inativos), edita, inativa e reativa. É o modelo das outras telas de cadastro. Revistas e
Clientes seguem o mesmo roteiro.

## Variável

| Nome | Linha | O que guarda |
|---|---|---|
| `livros` | 3 | Os livros que vieram de `GET /livro` |

## Funções

| Função | Linha | O que faz |
|---|---|---|
| `carregarLivros()` | 5 | Mostra "Carregando…", carrega as listas de apoio, preenche os selects e busca os livros |
| `preencherSelectsLivro()` | 20 | Preenche autor, editora e categoria, no formulário de cadastro e na janela de edição |
| `renderizarLivros()` | 30 | Filtra pela busca e pela chave "Mostrar inativos", clona o template para cada livro e liga os botões da linha |
| `validarFormLivro()` | 83 | Confere título, ISBN com 13 dígitos, ano, autor, editora e categoria |
| `abrirEdicaoLivro(livro)` | 120 | Preenche a janela de edição com os dados do livro. Recusa se o livro estiver inativo. |
| `inativarLivro(livro)` | 161 | Pede confirmação e chama `PATCH /livro/{id}/inativar` |
| `ativarLivro(livro)` | 179 | Chama `PATCH /livro/{id}/ativar` |

## Eventos

| Evento | Linha | O que acontece |
|---|---|---|
| `submit` em `#formLivro` | 95 | Valida, monta o `payload`, envia `POST /livro`, avisa e recarrega |
| `submit` em `#formEditarLivro` | 135 | Valida, envia `PATCH /livro/{id}`, fecha a janela e recarrega |
| `input` na busca | 189 | Redesenha a tabela a cada letra digitada (sem ir à API) |
| `change` em "Mostrar inativos" | 190 | Redesenha a tabela |
| `click` em ✏️ / 🚫 na linha | 60–70 | Abre a edição / inativa ou reativa aquele livro |

## Rotas da API

| Rota | Back-end chamado |
|---|---|
| `GET /livro` | `LivroService.visualizar()` |
| `POST /livro` | `LivroService.cadastrar()`, que cria `Livro(...)`; o construtor chama `super().__init__()` de `Material` |
| `PATCH /livro/{id}` | `Livro.atualizar()`, que sobrescreve o de `Material` e chama `super().atualizar(...)` |
| `PATCH /livro/{id}/inativar` / `ativar` | `Material.inativar()` / `ativar()` |

## O que é enviado no cadastro

```js
const payload = {
  titulo: "Dom Casmurro",
  isbn: "978-85-359-0277-1",   // o back-end tira pontos e hífens
  ano_publi: 1899,
  autor_id: 1, editora_id: 1, categoria_id: 1,
};
```

Os ids vêm dos selects, convertidos com `parseInt(valor, 10)`, porque o `value` de um campo é
sempre texto e o schema `SchemaLivroCadastro` espera inteiro.

## Regras conferidas antes de enviar

| Regra no front | Regra no back-end |
|---|---|
| ISBN com 13 dígitos (aceita `.` e `-`) | `Livro.normalizar_isbn()` + `_validar_isbn()` |
| Título obrigatório | `Material._validar_titulo_existente()` |
| Ano entre 1 e o ano atual | `Material._validar_ano_publi()` (barra ano ≤ 0) |
| Não edita livro inativo | `Material.atualizar()` lança "Material inativo não pode ser atualizado" |

## Detalhes

- **O título aparece com a primeira letra maiúscula** (`capitalizar`), porque o back-end grava
  em minúsculas (`_normalizar_titulo` faz `strip().lower()`).
- **O ISBN não aparece na edição.** O `SchemaLivroAtualizacao` não tem esse campo.
- **O botão da linha muda** conforme o livro: ativo mostra 🚫 Inativar (vermelho no hover),
  inativo mostra ⏻ Reativar.

## Recursos de JavaScript usados

- `template.content.cloneNode(true)` e `querySelector` dentro da cópia;
- `textContent` para escrever dados (seguro contra HTML);
- `classList.toggle("inativa", !livro.is_active)`;
- `addEventListener` com arrow function que "lembra" o livro da linha (closure);
- `filter` com duas condições combinadas (`&&`);
- `e.preventDefault()` para o formulário não recarregar a página;
- `e.target.reset()` para limpar o formulário depois do cadastro.

## Perguntas que podem cair na defesa

**Por que `e.preventDefault()` no submit?**
Sem ele, o navegador enviaria o formulário do jeito antigo e recarregaria a página. Com ele, o JS
envia por `fetch` e só atualiza a tabela.

**Como cada botão da tabela sabe de qual livro ele é?**
O `addEventListener("click", () => abrirEdicaoLivro(livro))` é criado dentro do `forEach`. A
arrow function guarda a variável `livro` daquela volta do laço (closure).

**A busca vai até a API?**
Não. `livros` já está em memória. A busca só filtra o array e redesenha a tabela.

**Onde aparece herança aqui?**
No back-end: `Livro` herda de `Material`. O formulário manda título, ano, editora e categoria
(atributos de `Material`) junto com ISBN e autor (só de `Livro`).
