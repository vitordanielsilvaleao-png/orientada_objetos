"""remove isbn da chave primária do livro

Revision ID: dbf83686c72c
Revises: eb118a43784a
Create Date: 2026-10-29 17:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'dbf83686c72c'
down_revision: Union[str, Sequence[str], None] = 'eb118a43784a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    #A troca é feita num único ALTER, pois a FK de livro.id para material.id depende do índice da chave primária
    #O isbn continua único pelo índice unique que já existe
    op.execute("ALTER TABLE livro DROP PRIMARY KEY, ADD PRIMARY KEY (id)")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TABLE livro DROP PRIMARY KEY, ADD PRIMARY KEY (id, isbn)")
