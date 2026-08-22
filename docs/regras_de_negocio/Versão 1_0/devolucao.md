Versão 1.0 - 22/08/2026

# Devoluções

### [RN-DEV-001] Registro de Devolução no MVP

No MVP, o bibliotecário será responsável por registrar as devoluções em nome dos usuários.

### [RN-DEV-002] Devolução de Empréstimo Ativo

Uma devolução somente poderá ser registrada para um empréstimo ativo.

### [RN-DEV-003] Devolução de Empréstimo Encerrado

Caso seja realizada uma tentativa de devolução de um empréstimo já encerrado, a operação deverá ser impedida e o motivo informado.

### [RN-DEV-004] Atualização da Disponibilidade

A devolução deverá atualizar automaticamente a disponibilidade do material de acordo com a existência de reservas ativas.

### [RN-DEV-005] Destinação de Material Reservado

Caso exista uma reserva ativa para o material devolvido, o status do material deverá ser alterado para reservado, e ele deverá ser destinado ao usuário que possuir a reserva ativa mais antiga.