"""add auth_user_id to conversations

Revision ID: 866d04a25f7b
Revises: 7a71d7c63ad7
Create Date: 2026-06-20 06:20:37.563595

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '866d04a25f7b'
down_revision: Union[str, Sequence[str], None] = '7a71d7c63ad7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Since we are adding a NOT NULL constraint to an existing table, clear data first
    op.execute("TRUNCATE TABLE conversations CASCADE")
    
    op.add_column("conversations", sa.Column("auth_user_id", sa.String(length=36), nullable=False))
    op.create_index("ix_conversations_auth_user_id", "conversations", ["auth_user_id"])
    op.create_foreign_key(
        "fk_conversations_auth_user_id", 
        "conversations", 
        "auth_users", 
        ["auth_user_id"], 
        ["id"], 
        ondelete="CASCADE"
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_conversations_auth_user_id", "conversations", type_="foreignkey")
    op.drop_index("ix_conversations_auth_user_id", table_name="conversations")
    op.drop_column("conversations", "auth_user_id")
