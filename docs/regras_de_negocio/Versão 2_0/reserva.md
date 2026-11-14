Versão 2.0 - 11/11/2026

# Circulação de Materiais do Acervo

## Reservas

### [RN-RES-001] Registro de Reserva
O registro de reservas é efetuado por intermédio do bibliotecário no sistema.

### [RN-RES-002] Reservas Simultâneas e Status da Reserva
Um usuário poderá possuir múltiplas reservas simultâneas para materiais distintos, sendo proibido possuir mais de uma reserva ativa (`ABERTA`) para o mesmo material simultaneamente. Os status possíveis da reserva compreendem: **ABERTA**, **ATENDIDA**, **CANCELADA** e **EXPIRADA**.

### [RN-RES-003] Concorrência de Reservas por Outros Usuários
A existência de uma reserva ativa por parte de um usuário não impede que outros usuários também registrem interesse, compondo a fila de espera (FIFO).

### [RN-RES-004] Prioridade da Fila de Reserva
Quando o material retornar ou estiver disponível, a reserva ativa mais antiga na fila de espera (respeitando a ordem cronológica) terá prioridade de atendimento.

### [RN-RES-005] Prazo de Validade da Reserva
Uma reserva ativa (`ABERTA`) permanecerá válida pelo período máximo de 10 dias.

### [RN-RES-006] Cancelamento Automático da Reserva (Expiração)
Caso uma reserva ativa não seja atendida dentro do prazo limite de 10 dias, seu status mudará automaticamente para **EXPIRADA**, liberando a vaga para o próximo da fila.

### [RN-RES-007] Cancelamento de Reserva Ativa
Uma reserva somente poderá ser cancelada pelo operador/usuário enquanto estiver com o status `ABERTA` na fila.