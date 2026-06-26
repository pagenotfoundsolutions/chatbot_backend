from abc import ABC, abstractmethod
from typing import Sequence

from app.modules.rag.application.queries.search_chunks.search_chunks_query import SearchChunksQuery
from app.modules.rag.domain.entities.document_chunk import DocumentChunk

class SearchChunksUseCase(ABC):
    """Input port for searching similar document chunks."""

    @abstractmethod
    def execute(self, query: SearchChunksQuery) -> Sequence[DocumentChunk]:
        pass
