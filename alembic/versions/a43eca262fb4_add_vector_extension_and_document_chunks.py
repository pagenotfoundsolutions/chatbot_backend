"""add_vector_extension_and_document_chunks

Revision ID: a43eca262fb4
Revises: 45566f02f81b
Create Date: 2026-06-23 22:26:27.283703

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a43eca262fb4'
down_revision: Union[str, Sequence[str], None] = '45566f02f81b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('CREATE EXTENSION IF NOT EXISTS vector;')
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    
    op.execute('''
        CREATE TABLE IF NOT EXISTS langchain_pg_collection (
            uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            name VARCHAR,
            cmetadata JSONB
        );
    ''')
    
    op.execute('''
        CREATE TABLE IF NOT EXISTS langchain_pg_embedding (
            uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            collection_id UUID REFERENCES langchain_pg_collection(uuid) ON DELETE CASCADE,
            embedding VECTOR,
            document VARCHAR,
            cmetadata JSONB,
            custom_id VARCHAR
        );
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('DROP TABLE IF EXISTS langchain_pg_embedding;')
    op.execute('DROP TABLE IF EXISTS langchain_pg_collection;')
    op.execute('DROP EXTENSION IF EXISTS vector;')
