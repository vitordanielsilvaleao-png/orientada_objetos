Versão 2.0 - 11/11/2026

# Devoluções

### [RN-DEV-001] Registro de Devolução por Bibliotecário
O bibliotecário é responsável por registrar as devoluções em nome dos usuários no sistema.

### [RN-DEV-002] Devolução de Empréstimo Ativo
Uma devolução somente poderá ser registrada para um empréstimo que esteja com status ativo.

### [RN-DEV-003] Devolução de Empréstimo Encerrado
Caso seja realizada uma tentativa de devolução de um empréstimo já encerrado ou cancelado, a operação deverá ser impedida e o motivo informado.

### [RN-DEV-004] Atualização Automática da Disponibilidade e Fila
A devolução deverá atualizar automaticamente a disponibilidade do material e verificar imediatamente a existência de reservas pendentes na fila de espera.

### [RN-DEV-005] Destinação de Material Reservado e Gestão da Fila
Caso exista uma reserva ativa para o material devolvido, o sistema deverá processar a fila FIFO: a reserva mais antiga do usuário correspondente terá seu status alterado para atendida/reservada para retirada, e o material será destinado prioritariamente a esse usuário, ajustando os contadores de disponibilidade adequadamente.