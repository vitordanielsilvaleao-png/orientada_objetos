# `js/emprestimos.js`

## Para que serve

Tela de **Empréstimos**. O registro é feito em **2 etapas**, como o cadastro em etapas da
oficina (Cliente → Veículo → Serviço):

1. **Cliente:** escolhe quem vai levar. A tela confere as regras do limite e do atraso.
2. **Material:** escolhe o livro ou a revista entre os que podem sair para aquele cliente.

A tela também lista os empréstimos em três abas (Em aberto, Atrasados, Todos), com busca, e
registra a devolução.

## Constantes e variáveis

| Nome | Linha | O que guarda |
|---|---|---|
| `LIMITE_EMPRESTIMOS` | 3 | 4, o mesmo limite do `EmprestimoService.cadastrar()` |
| `emprestimos` | 5 | Lista da aba escolhida |
| `todosEmprestimos` | 6 | Todos os empréstimos, para contar os ativos de cada cliente |
| `reservasAtivas` | 7 | Reservas abertas, para liberar o material RESERVADO para quem reservou |
| `filtroEmprestimos` | 8 | Aba atual: `"abertos"`, `"atrasados"` ou `"todos"` |
| `clienteEmprestimo` | 9 | Cliente escolhido na etapa 1 (`null` enquanto ninguém foi escolhido) |
| `CAMINHOS_EMPRESTIMO` | 11 | Rota da API de cada aba |

## Funções

| Função | Linha | O que faz |
|---|---|---|
| `carregarEmprestimos()` | 17 | Busca a lista da aba, todos os empréstimos e as reservas abertas (3 rotas juntas) e preenche o select de clientes ativos |
| `renderizarEmprestimos()` | 41 | Filtra pela busca e desenha as linhas. O botão "Registrar devolução" só aparece nos ativos. |
| `emprestimosAtivosDo(clienteId)` | 84 | Empréstimos ativos (ABERTO ou ATRASADO) do cliente |
| `ativarEtapaMaterial(cliente, quantidadeAtivos)` | 110 | Conclui a etapa 1: mostra o chip "Ana Souza · 2 empréstimos ativos de 4", libera o `fieldset` da etapa 2 e troca o "1" por ✓ |
| `resetarEtapaCliente()` | 125 | Volta tudo para a etapa 1 |
| `materialPodeSerEmprestado(material)` | 144 | `true` se o material está ativo e DISPONIVEL, ou RESERVADO por uma reserva deste cliente |
| `atualizarMateriaisEmprestimo()` | 151 | Preenche o select da etapa 2 só com os materiais que passam na função acima |
| `devolverEmprestimo(emprestimo)` | 189 | Pede confirmação e chama `PATCH /emprestimo/{id}/devolver` |
| `definirFiltroEmprestimos(filtro)` | 213 | Só marca a aba (usado também pelo link "Atrasados" do Painel) |
| `selecionarFiltroEmprestimos(filtro)` | 220 | Marca a aba e recarrega a lista |

## Eventos

| Evento | Linha | O que acontece |
|---|---|---|
| `submit` em `#formEmpCliente` (etapa 1) | 88 | Valida o cliente e confere as regras |
| `click` em ✏️ do chip | 139 | Troca o cliente |
| `submit` em `#formEmprestimo` (etapa 2) | 158 | Envia `POST /emprestimo` |
| `click` nas abas | 208 | Troca o filtro |
| `input` na busca | 225 | Redesenha a tabela |

## As regras da etapa 1, lado a lado com o back-end

```js
const ativos = emprestimosAtivosDo(id);
if (ativos.some((emp) => emp.status === "ATRASADO")) { ... }   // tem atraso: bloqueia
if (ativos.length >= LIMITE_EMPRESTIMOS) { ... }                // já tem 4: bloqueia
```

No `EmprestimoService.cadastrar()`, o mesmo laço percorre os empréstimos ativos do cliente,
conta (`cont_emprestimos += 1`) e lança 409 se achar um ATRASADO ou se a conta chegar a 4. O
front só avisa antes. Se alguém burlar, o back-end barra do mesmo jeito.

## Por que um material RESERVADO pode aparecer na etapa 2

O back-end aceita emprestar um material RESERVADO quando a reserva ativa daquele material é do
mesmo cliente. Nesse caso, o empréstimo também encerra a reserva (`reserva.concluir()`). Por
isso `materialPodeSerEmprestado` procura em `reservasAtivas` uma reserva com aquele
`material_id` e aquele `cliente_id`.

## Rotas da API

| Rota | Back-end chamado |
|---|---|
| `GET /emprestimo` / `abertos` / `atrasados` | `EmprestimoService.visualizar()` / `visualizar_abertos()` / `visualizar_atrasados()` |
| `GET /reserva/abertas` | `ReservaService.visualizar_abertos()` |
| `POST /emprestimo` | `EmprestimoService.cadastrar()`: cria `Emprestimo(...)` e chama `material.emprestar()` |
| `PATCH /emprestimo/{id}/devolver` | `EmprestimoService.registrar_devolucao()`: chama `Emprestimo.devolver()` e passa o material para a reserva mais antiga do mesmo título, se houver |

## Recursos de JavaScript usados

- `some()` para "existe algum atrasado?";
- `filter` + `length` para contar;
- `<fieldset disabled>`, que trava todos os campos de uma vez, e `fieldset.disabled = false` para liberar;
- `hidden` em elementos (o formulário da etapa 1 some, o chip aparece);
- `setTimeout(resetarEtapaCliente, 1400)` para mostrar o ✓ antes de voltar ao início;
- `innerHTML = '<i class="fa-solid fa-check"></i>'` para trocar o número da etapa pelo ícone;
- `remove()` para tirar da linha o botão de devolução dos empréstimos encerrados.

## Perguntas que podem cair na defesa

**Por que dividir em etapas?**
O cliente decide quais materiais podem sair: um RESERVADO só sai para quem reservou. Escolhendo
o cliente primeiro, a etapa 2 já mostra só o que é permitido. É o mesmo raciocínio da oficina,
em que a ordem só é criada depois do cliente.

**O front calcula o atraso?**
Não. O status ATRASADO vem pronto do back-end, onde o agendador roda `marcar_atrasado()` de hora
em hora. O front só calcula a data "Devolver até" (`prazoDevolucao`), para mostrar na tabela.

**O que acontece na devolução se alguém reservou o mesmo título?**
O back-end não deixa o material DISPONIVEL: marca como RESERVADO e vincula à reserva mais antiga.
Na tela de Reservas, a coluna "Exemplar" passa a mostrar "Separado".
