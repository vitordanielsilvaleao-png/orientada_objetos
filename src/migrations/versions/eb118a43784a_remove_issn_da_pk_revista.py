"""remove issn da chave primária da revista

Revision ID: eb118a43784a
Revises: 98ea26be709f
Create Date: 2026-10-29 16:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'eb118a43784a'
down_revision: Union[str, Sequence[str], None] = '98ea26be709f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    #A troca é feita num único ALTER, pois a FK de revista.id para material.id depende do índice da chave primária
    #O issn continua único pelo índice unique que já existe
    op.execute("ALTER TABLE revista DROP PRIMARY KEY, ADD PRIMARY KEY (id)")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TABLE revista DROP PRIMARY KEY, ADD PRIMARY KEY (id, issn)")
