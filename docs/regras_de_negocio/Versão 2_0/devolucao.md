Versão 2.0 - 11/11/2026

# Devoluções

### [RN-DEV-001] Registro de Devolução por Bibliotecário
O bibliotecário é responsável por registrar as devoluções em nome dos usuários no sistema.

### [RN-DEV-002] Devolução de Empréstimo Ativo
Uma devolução somente poderá ser registrada para um empréstimo que esteja com status ativo.

### [RN-DEV-003] Devolução de Empréstimo Encerrado
Caso seja realizada uma tentativa de devolução de um empréstimo já encerrado ou cancelado, a operação deverá ser impedida e o motivo informado.

### [RN-DEV-004] Atualização do Status do Exemplar
A devolução deverá atualizar automaticamente o status do exemplar para `DISPONIVEL` ou `RESERVADO`, dependendo da existência de reservas pendentes.

### [RN-DEV-005] Destinação de Material Reservado e Vínculo de Reserva
Caso exista uma reserva ativa (status `ABERTA`) para o material devolvido, a devolução vincula o material à reserva e altera o status do exemplar para `RESERVADO`. A reserva em si passa a ter o status `ATENDIDA` somente no momento em que o empréstimo correspondente for realizado.