Versão 2.0 - 11/11/2026

# Devoluções

### [RN-DEV-001] Registro de Devolução por Bibliotecário
O bibliotecário é responsável por registrar as devoluções em nome dos usuários no sistema.

### [RN-DEV-002] Devolução de Empréstimo Ativo
Uma devolução somente poderá ser registrada para um empréstimo que esteja com status ativo.

### [RN-DEV-003] Devolução de Empréstimo Encerrado
Caso seja realizada uma tentativa de devolução de um empréstimo já encerrado ou cancelado, a operação deverá ser impedida e o motivo informado.

### [RN-DEV-004] Atualização do Status do Exemplar
A devolução deverá atualizar automaticamente o status do exemplar para `DISPONIVEL` ou `RESERVADO`, dependendo da existência de reservas pendentes na fila.

### [RN-DEV-005] Destinação de Material Reservado na Devolução
Caso exista uma reserva ativa (`ABERTA`) para o material devolvido, o sistema vincula o exemplar à reserva e altera o status do exemplar para `RESERVADO`. A reserva em si continuará aguardando e só passará para o status `ATENDIDA` no momento em que o empréstimo correspondente for efetivamente realizado.