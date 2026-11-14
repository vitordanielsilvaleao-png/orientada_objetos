# `js/reservas.js`

## Para que serve

Tela de **Reservas**: registra uma reserva por **título** (não por exemplar), lista as reservas
em três abas (Abertas, Expiradas, Todas), com busca, e permite **atender** ou **cancelar**.

A reserva pode ser de um título que **ainda não está no acervo**. Quando esse livro ou revista
for cadastrado, o back-end separa o exemplar para a reserva mais antiga.

## Variáveis e constante

| Nome | Linha | O que guarda |
|---|---|---|
| `reservas` | 3 | Lista da aba escolhida |
| `filtroReservas` | 4 | Aba atual: `"abertas"`, `"expiradas"` ou `"todas"` |
| `CAMINHOS_RESERVA` | 6 | Rota da API de cada aba |

## Funções

| Função | Linha | O que faz |
|---|---|---|
| `carregarReservas()` | 12 | Carrega as listas de apoio, preenche o select de clientes ativos e as sugestões de título, e busca as reservas da aba |
| `preencherSugestoesTitulo()` | 30 | Monta o `<datalist>` com os títulos do acervo, sem repetir (`new Set`) |
| `tituloNoAcervo(titulo)` | 37 | Diz se existe material ativo com aquele título, comparando do jeito do back-end (sem espaços nas pontas e em minúsculas) |
| `renderizarReservas()` | 42 | Desenha as linhas, escreve a situação do exemplar e mostra os botões certos |
| `atenderReserva(reserva)` | 124 | Pede confirmação e chama `PATCH /reserva/{id}` |
| `cancelarReserva(reserva)` | 141 | Pede confirmação e chama `PATCH /reserva/{id}/cancelar` |

## Eventos

| Evento | Linha | O que acontece |
|---|---|---|
| `submit` em `#formReserva` | 90 | Valida cliente e título, envia `POST /reserva` e escolhe a mensagem do aviso |
| `click` nas abas | 159 | Troca o filtro e recarrega |
| `input` na busca | final do arquivo | Redesenha a tabela |

## A coluna "Exemplar"

| O que aparece | Quando |
|---|---|
| **Separado (nº 12)** | A reserva já tem `material_id`: o exemplar está guardado para o cliente e o botão **Atender** aparece |
| **Aguardando devolução** | O título existe no acervo, mas todos os exemplares estão emprestados |
| **Fora do acervo** | Nenhum material ativo tem esse título; a reserva espera o cadastro |

## O aviso depois de reservar

| Resposta da API | Mensagem |
|---|---|
| `data.material_id` preenchido | "Havia um exemplar disponível, e ele já ficou separado." |
| Sem exemplar, título no acervo | "O cliente entra na fila até um exemplar ser devolvido." |
| Sem exemplar, título fora do acervo | "O título ainda não está no acervo: o exemplar será separado quando ele for cadastrado." |

## Como o exemplar chega até a reserva (back-end)

1. **Na hora de reservar** (`ReservaService.cadastrar`): se houver exemplar DISPONIVEL com o mesmo
   título, ele é vinculado na hora, e `material.reservar()` muda o status para RESERVADO.
2. **Na devolução** (`EmprestimoService.registrar_devolucao`): se houver reserva aberta sem
   exemplar para aquele título, o material devolvido vai para a **mais antiga**
   (`order_by(Reserva.data.asc())`).
3. **No cadastro de um livro ou revista novo** (`LivroService.cadastrar` /
   `RevistaService.cadastrar`): a mesma busca pela reserva mais antiga sem exemplar. Se achar, o
   material já nasce RESERVADO.
4. **Expiração:** a reserva vale 10 dias. O agendador chama `verificar_expiracao()` de hora em
   hora, e a reserva vencida vai para a aba "Expiradas".

## Rotas da API

| Rota | Back-end chamado |
|---|---|
| `GET /reserva` / `abertas` / `expiradas` | `ReservaService.visualizar()` / `visualizar_abertos()` / `visualizar_expiradas()` |
| `POST /reserva` | `ReservaService.cadastrar()` |
| `PATCH /reserva/{id}` | `ReservaService.atender_reserva()`: cria um `EmprestimoService` e chama o `cadastrar()` dele |
| `PATCH /reserva/{id}/cancelar` | `ReservaService.inativar()` → `Reserva.cancelar()` |

## Cuidado: o título precisa bater

O back-end compara títulos só com `strip().lower()`. "Memorias" (sem acento) e "Memórias" são
títulos diferentes. Por isso o campo tem sugestões (`<datalist>`) com os títulos que já existem.
Num título novo, o bibliotecário precisa digitar igual ao que será cadastrado depois.

## Recursos de JavaScript usados

- `<datalist>` ligado ao `<input list="listaTitulos">` (autocompletar nativo);
- `new Set(...)` + spread (`[...new Set(lista)]`) para tirar títulos repetidos;
- `let mensagem` com `if / else if` para escolher o aviso;
- `remove()` para tirar da linha os botões que não se aplicam;
- `setAttribute("aria-selected", ...)` para marcar a aba ativa (acessibilidade).

## Perguntas que podem cair na defesa

**Por que a reserva é por título e não por exemplar?**
O cliente quer "Dom Casmurro", qualquer exemplar. O sistema separa o primeiro que ficar livre.

**Por que "Atender" só aparece em algumas reservas?**
Atender cria o empréstimo do exemplar separado. Sem exemplar vinculado, não há o que emprestar,
e o back-end responderia 404 ("Reserva não possui material associado").

**Onde um service usa outro?**
`ReservaService.atender_reserva()` cria um `EmprestimoService(self.session)` e chama o
`cadastrar()` dele. Assim as regras do empréstimo (limite de 4, atraso) valem também para a
reserva atendida, sem repetir código.

**Dá para reservar um livro que a biblioteca ainda não tem?**
Sim. A coluna mostra "Fora do acervo" e, quando o livro for cadastrado, o `LivroService` vincula
o exemplar à reserva mais antiga. Se isso não acontecer em 10 dias, a reserva expira.
