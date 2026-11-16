Versão 2.0 - 16/11/2026

# Circulação de Materiais do Acervo

## Reservas

### [RN-RES-001] Registro de Reserva
O registro de reservas é efetuado por intermédio do bibliotecário no sistema.

### [RN-RES-002] Reservas Simultâneas e Status da Reserva
Um usuário poderá possuir múltiplas reservas simultâneas para materiais distintos, sendo proibido possuir mais de uma reserva com status `ABERTA` para o mesmo material simultaneamente. Os status possíveis da reserva no código compreendem: **ABERTA**, **ATENDIDA**, **CANCELADA** e **EXPIRADA**.

### [RN-RES-003] Concorrência de Reservas por Outros Usuários
A existência de uma reserva ativa (`ABERTA`) por parte de um usuário não impede que outros usuários também registrem interesse, compondo a fila de espera (FIFO).

### [RN-RES-004] Prioridade da Fila de Reserva
Quando o material retornar ou estiver disponível, a reserva mais antiga na fila de espera com status `ABERTA` (respeitando a ordem cronológica) terá prioridade de atendimento.

### [RN-RES-005] Prazo de Validade da Reserva
Uma reserva com status `ABERTA` permanecerá válida pelo período máximo de 10 dias.

### [RN-RES-006] Expiração Automática da Reserva
Caso uma reserva `ABERTA` não seja atendida dentro do prazo limite de 10 dias, o método `verificar_expiracao()` altera automaticamente o status da reserva para **EXPIRADA**.
* **Pendência conhecida na Versão 2.0:** Atualmente, a rotina de expiração altera apenas o status da reserva, mantendo o material com status `RESERVADO` sem transferi-lo automaticamente para o próximo da fila ou retorná-lo para `DISPONIVEL`.

### [RN-RES-007] Cancelamento de Reserva Ativa
Uma reserva somente poderá ser cancelada pelo operador/usuário enquanto estiver com o status `ABERTA` na fila.