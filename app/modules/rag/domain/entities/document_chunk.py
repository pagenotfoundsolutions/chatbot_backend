import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from app.shared.kernel.aggregate_root import AggregateRoot

class DocumentChunk(AggregateRoot[uuid.UUID]):
    """Domain entity representing a chunk of text and its embedding."""
    
    def __init__(
        self,
        id: uuid.UUID,
        file_id: uuid.UUID,
        auth_user_id: uuid.UUID,
        content: str,
        chunk_index: int = 0,
        page_number: Optional[int] = None,
        embedding: Optional[list[float]] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        super().__init__(id)
        self.file_id = file_id
        self.auth_user_id = auth_user_id
        self.content = content
        self.chunk_index = chunk_index
        self.page_number = page_number
        self.embedding = embedding
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

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
