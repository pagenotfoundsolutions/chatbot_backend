from abc import ABC, abstractmethod
import uuid
from typing import Sequence, Optional

from app.modules.rag.domain.entities.document_chunk import DocumentChunk

class VectorStorePort(ABC):
    """Output port for storing and retrieving DocumentChunks from a vector database."""

    @abstractmethod
    def save_chunks(self, chunks: Sequence[DocumentChunk]) -> None:
        """Saves multiple document chunks to the vector store."""
        pass

    @abstractmethod
    def search_similar(
        self, 
        query_embedding: list[float], 
        top_k: int = 5, 
        auth_user_id: Optional[uuid.UUID] = None,
        file_id: Optional[uuid.UUID] = None,
        query_text: Optional[str] = None
    ) -> Sequence[DocumentChunk]:
        """Performs a similarity search using an embedding vector and optional keyword search.
        Can optionally filter by user and file.
        """
        pass

    @abstractmethod
    def delete_by_file_id(self, file_id: uuid.UUID) -> None:
        """Deletes all chunks associated with a specific file."""
        pass
