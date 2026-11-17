# Missão 14 — Coleções, Listas e Enums de Status

## Objetivo e planejamento

A décima quarta missão teve como objetivo a consolidação do sistema através da implementação de coleções, listagens especializadas, Enums de status para controle de domínio e a lógica de fila de reservas integrada com o fluxo de empréstimos.

Nesta etapa, o foco foi estruturar de forma padronizada os estados possíveis de cada entidade (`Material`, `Emprestimo` e `Reserva`) utilizando a biblioteca `Enum` do Python, além de fornecer mecanismos robustos para listagem e filtragem de registros ativos, atrasados e expirados.

O objetivo principal foi garantir a integridade dos dados, eliminar o uso de strings mágicas no código e automatizar o fluxo de atendimento de reservas quando um material retorna ao acervo.

---

## O que foi implementado e por quê

Nessa missão foram desenvolvidas as seguintes melhorias estruturais no código:

- **Enums de Status (`src/compartilhado/enum.py`)**:
  - `StatusMaterial`: Padronização dos estados `DISPONIVEL`, `EMPRESTADO` e `RESERVADO`.
  - `StatusEmprestimo`: Padronização dos estados `ABERTO`, `DEVOLVIDO` e `ATRASADO`.
  - `StatusReserva`: Padronização dos estados `ABERTA`, `ATENDIDA`, `CANCELADA` e `EXPIRADA`.

- **Gerenciamento de Empréstimos (`EmprestimoService`)**:
  - Implementação de listagens para empréstimos abertos e empréstimos em atraso baseadas em filtragens de coleções e verificação de prazos.
  - Regra de validação de limite máximo de empréstimos ativos por cliente (limite de 4 itens).
  - Vinculação e encerramento automático da reserva ativa do cliente no momento em que o empréstimo é cadastrado.

- **Fila de Reservas e Gestão (`ReservaService`)**:
  - Implementação de listagens para reservas ativas e expiradas.
  - Lógica inteligente de devolução e fila de espera: ao registrar a devolução de um material, o sistema verifica se existe alguma reserva pendente. Caso exista, o material é automaticamente direcionado para o status de reservado e vinculado à próxima reserva da fila; caso contrário, o material retorna ao status de disponível.

---

## Decisões técnicas e trade-offs

Durante esta etapa, algumas decisões de arquitetura e design foram tomadas para garantir a robustez e manutenibilidade do sistema:

- **Uso de Enums em vez de Strings Brutas**:
  Inicialmente, os estados dos objetos eram representados por strings literais espalhadas pelo código. 
  Optou-se por centralizar e tipar esses estados utilizando `Enum` do Python. 
  Essa decisão elimina o risco de erros de digitação (typos) em comparações de status e melhora significativamente a legibilidade do código e o suporte do editor.

- **Automação da Fila de Reservas na Devolução**:
  Para evitar processos manuais na biblioteca, a lógica de verificação de reservas pendentes foi embutida diretamente no método de devolução do empréstimo (`registrar_devolucao`). 
  Isso garante que o acervo se mantenha sincronizado e que os usuários na fila de espera sejam atendidos de forma justa e automática.

---

## Dificuldades encontradas e soluções

Uma das principais dificuldades encontradas foi gerenciar a transição de estados entre o material devolvido e a verificação de existência de reservas pendentes sem gerar inconsistências na base de dados.

Como solução, utilizou-se o escopo transacional da sessão do SQLAlchemy (`self.session.commit()` e `self.session.refresh()`), garantindo que a alteração de status do material, a conclusão da reserva e o registro do empréstimo ocorram de forma atômica e segura.

---

## Reflexão sobre o conceito aprendido

A décima quarta missão permitiu compreender a importância de estruturar adequadamente o domínio utilizando coleções e tipos enumerados (`Enum`). 

A principal aprendizagem foi perceber que regras de negócio complexas — como o gerenciamento de filas de espera e limites de empréstimos — tornam-se muito mais fáceis de manter e testar quando os estados do sistema são rigidamente definidos e isolados nas respectivas entidades e serviços.

---

## Commit(s) associado(s)

feat: implementa colecoes, listagens, fila de reservas e enums de status da missao 14