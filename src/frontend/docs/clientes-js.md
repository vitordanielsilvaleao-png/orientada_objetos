# `js/clientes.js`

## Para que serve

Tela de **Clientes** (os leitores): cadastra, lista (com busca e inativos), edita, inativa e
reativa. Cliente nunca é apagado, só inativado, para o histórico de empréstimos continuar
ligado a ele.

## Funções

| Função | Linha | O que faz |
|---|---|---|
| `carregarClientes()` | 3 | Busca `GET /cliente` e guarda na lista `clientes` do `geral.js`, a mesma usada pelas outras telas |
| `formatarCpf(cpf)` | 15 | `12345678909` → `123.456.789-09` |
| `formatarTelefone(tel)` | 19 | `34999990000` → `(34) 99999-0000` (aceita 10 ou 11 dígitos) |
| `renderizarClientes()` | 26 | Filtra, ordena por nome, clona o template e liga os botões |
| `validarDadosCliente(prefixo, comCpf)` | 77 | Valida nome (≥ 3 letras), CPF (11 dígitos, só no cadastro), telefone (10 ou 11), rua, número > 0 e bairro |
| `lerDadosCliente(prefixo)` | 91 | Lê os campos e monta o objeto. Complemento vazio vira `null`. |
| `abrirEdicaoCliente(cliente)` | 122 | Preenche a janela de edição (sem CPF) |
| `inativarCliente(cliente)` / `ativarCliente(cliente)` | 154 / 172 | `PATCH /cliente/{id}/inativar` / `ativar` |

## Eventos

| Evento | Linha | O que acontece |
|---|---|---|
| `submit` em `#formCliente` | 103 | Valida, envia `POST /cliente` com o CPF |
| `submit` em `#formEditarCliente` | 134 | Valida, envia `PATCH /cliente/{id}` sem o CPF |
| `input` na busca / `change` em "Mostrar inativos" | 182–183 | Redesenha a tabela |

## Um código para dois formulários

Cadastro e edição têm os mesmos campos com prefixos diferentes nos ids (`cliNome` /
`editClienteNome`). Por isso `validarDadosCliente` e `lerDadosCliente` recebem o prefixo e
montam o id com template string:

```js
document.getElementById(`${prefixo}Telefone`).value
```

E o cadastro junta o CPF ao resto com spread:

```js
const payload = { ...lerDadosCliente("cli"), cpf: document.getElementById("cliCpf").value.trim() };
```

## Regras conferidas antes de enviar

| Regra no front | Regra na entidade `Cliente` |
|---|---|
| Nome com pelo menos 3 letras | `normalizar_nome()` + `_validar_nome()` |
| CPF com 11 dígitos (aceita `.` e `-`) | `@validates("_cpf")` → `normalizar_cpf()` + `_validar_cpf()` |
| Telefone com 10 ou 11 dígitos | `normalizar_telefone()` + `_validar_telefone()` |
| Número maior que zero | `normalizar_numero()` + `_validar_numero()` |

CPF repetido não é conferido no front: quem responde é o back-end, e a tela mostra a mensagem dele.

## Encapsulamento visto pela tela

- **O CPF não aparece na janela de edição.** Na entidade, o CPF fica em `_cpf` e é lido pela
  `@hybrid_property cpf`, que não tem setter. O `SchemaClienteAtualizacao` também não tem o
  campo.
- **A situação muda por métodos.** "Ativo / Inativo" só muda pelos métodos
  `inativar_cliente()` e `ativar_cliente()`. O front não manda `is_active` em lugar nenhum.

## Rotas da API

| Rota | Back-end chamado |
|---|---|
| `GET /cliente` | `ClienteService.visualizar()` |
| `POST /cliente` | `ClienteService.cadastrar()`, que cria `Cliente(...)` |
| `PATCH /cliente/{id}` | `Cliente.atualizar_cliente()` |
| `PATCH /cliente/{id}/inativar` / `ativar` | `Cliente.inativar_cliente()` / `ativar_cliente()` |

## Recursos de JavaScript usados

- template string para montar ids (`` `${prefixo}Nome` ``);
- spread de objeto (`{ ...dados, cpf }`);
- `slice` para formatar CPF e telefone;
- `filter(Boolean)` para pular complemento vazio ao montar o endereço;
- `||` para trocar texto vazio por `null` (`complemento || null`);
- `sort` com `localeCompare`.

## Perguntas que podem cair na defesa

**Por que não dá para editar o CPF?**
Porque a regra do sistema é que o CPF identifica o cliente e não muda. No back-end, isso é
encapsulamento: `_cpf` é privado e só tem getter.

**Por que inativar em vez de excluir?**
O cliente tem empréstimos e reservas ligados pelo `cliente_id`. Excluir quebraria esse
histórico. Inativo, ele só fica impedido de fazer novos empréstimos e reservas.

**Por que o front tira a pontuação só para contar os dígitos, mas envia o CPF como foi digitado?**
Quem normaliza é a entidade (`normalizar_cpf`). O front só confere se há 11 dígitos, para avisar
antes.
