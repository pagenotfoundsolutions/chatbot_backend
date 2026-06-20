"""add deleted_at to conversations

Revision ID: 3f73605a7fc5
Revises: 866d04a25f7b
Create Date: 2026-06-20 06:30:30.139285

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f73605a7fc5'
down_revision: Union[str, Sequence[str], None] = '866d04a25f7b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("conversations", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("conversations", "deleted_at")
