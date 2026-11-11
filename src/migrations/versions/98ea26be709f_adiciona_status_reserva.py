"""adiciona status na reserva

Revision ID: 98ea26be709f
Revises: 0c774de4eddb
Create Date: 2026-10-29 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '98ea26be709f'
down_revision: Union[str, Sequence[str], None] = '0c774de4eddb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

status_reserva = sa.Enum('ABERTA', 'ATENDIDA', 'CANCELADA', 'EXPIRADA', name='statusreserva')


def upgrade() -> None:
    """Upgrade schema."""
    #O server_default preenche as reservas já existentes; é removido logo depois, como na coluna status do emprestimo
    op.add_column('reserva', sa.Column('status', status_reserva, server_default='ABERTA', nullable=False))

    #Não há como saber se uma reserva inativa antiga foi atendida, cancelada ou expirou; todas viram CANCELADA
    op.execute("UPDATE reserva SET status = 'CANCELADA' WHERE is_active = 0")

    op.alter_column('reserva', 'status', existing_type=status_reserva, existing_nullable=False, server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('reserva', 'status')
