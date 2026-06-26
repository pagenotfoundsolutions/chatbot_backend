import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from app.shared.kernel.aggregate_root import AggregateRoot

@dataclass(kw_only=True)
class DocumentChunk(AggregateRoot[uuid.UUID]):
    """Domain entity representing a chunk of text and its embedding."""
    
    file_id: uuid.UUID
    auth_user_id: uuid.UUID
    content: str
    
    # Embedding is kept as list of floats (vector).
    # Might be None initially before embedding generation.
    embedding: Optional[list[float]] = None
    
    # Metadata
    page_number: Optional[int] = None
    chunk_index: int = 0
    
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    @classmethod
    def create(
        cls,
        file_id: uuid.UUID,
        auth_user_id: uuid.UUID,
        content: str,
        chunk_index: int,
        page_number: Optional[int] = None,
        embedding: Optional[list[float]] = None,
    ) -> "DocumentChunk":
        chunk_id = uuid.uuid4()
        chunk = cls(
            id=chunk_id,
            file_id=file_id,
            auth_user_id=auth_user_id,
            content=content,
            chunk_index=chunk_index,
            page_number=page_number,
            embedding=embedding,
        )
        return chunk
