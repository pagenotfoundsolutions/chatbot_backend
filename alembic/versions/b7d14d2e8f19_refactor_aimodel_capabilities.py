"""refactor AIModel capabilities to JSON array

Revision ID: b7d14d2e8f19
Revises: a73e5427cba5
Create Date: 2026-06-27 23:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b7d14d2e8f19'
down_revision: Union[str, None] = 'a73e5427cba5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add capabilities column
    op.add_column('ai_models', sa.Column('capabilities', sa.JSON(), nullable=True))
    
    # Optional: data migration script can be added here if we wanted to preserve existing booleans
    # For now, we update it to an empty list as default so we can make it non-nullable later
    op.execute("UPDATE ai_models SET capabilities = '[]'::json")
    
    # Make capabilities non-nullable
    op.alter_column('ai_models', 'capabilities', nullable=False)
    
    # Drop old boolean columns
    columns_to_drop = [
        'supports_tools', 'supports_parallel_tools', 'supports_structured_output', 
        'supports_json', 'supports_stream', 'supports_vision', 'supports_image_generation', 
        'supports_audio_input', 'supports_audio_output', 'supports_embeddings', 
        'supports_reasoning', 'supports_system_prompt', 'supports_web_search', 
        'supports_file_upload', 'supports_pdf', 'supports_function_call', 'supports_seed', 
        'supports_response_format', 'supports_cache', 'supports_citations', 'supports_multimodal'
    ]
    for col in columns_to_drop:
        op.drop_column('ai_models', col)


def downgrade() -> None:
    # Re-add boolean columns with default False
    columns_to_add = [
        'supports_tools', 'supports_parallel_tools', 'supports_structured_output', 
        'supports_json', 'supports_vision', 'supports_image_generation', 
        'supports_audio_input', 'supports_audio_output', 'supports_embeddings', 
        'supports_reasoning', 'supports_web_search', 'supports_file_upload', 
        'supports_pdf', 'supports_function_call', 'supports_seed', 
        'supports_response_format', 'supports_cache', 'supports_citations', 'supports_multimodal'
    ]
    for col in columns_to_add:
        op.add_column('ai_models', sa.Column(col, sa.Boolean(), server_default='false', nullable=False))
        
    # Re-add stream and system_prompt which default to True
    op.add_column('ai_models', sa.Column('supports_stream', sa.Boolean(), server_default='true', nullable=False))
    op.add_column('ai_models', sa.Column('supports_system_prompt', sa.Boolean(), server_default='true', nullable=False))
    
    # Drop capabilities column
    op.drop_column('ai_models', 'capabilities')
