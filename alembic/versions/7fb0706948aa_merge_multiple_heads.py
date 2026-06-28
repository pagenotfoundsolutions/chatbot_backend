"""merge multiple heads

Revision ID: 7fb0706948aa
Revises: a6044ac73400, b7d14d2e8f19
Create Date: 2026-06-28 16:35:26.957451

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7fb0706948aa'
down_revision: Union[str, Sequence[str], None] = ('a6044ac73400', 'b7d14d2e8f19')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
