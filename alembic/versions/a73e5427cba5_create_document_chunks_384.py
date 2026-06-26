"""create_document_chunks_384

Revision ID: a73e5427cba5
Revises: a43eca262fb4
Create Date: 2026-06-26 02:52:16.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector


# revision identifiers, used by Alembic.
revision: str = 'a73e5427cba5'
down_revision: Union[str, Sequence[str], None] = 'a43eca262fb4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass

def downgrade() -> None:
    pass
