from abc import ABC, abstractmethod
from typing import Sequence
from app.modules.rag.application.dto.chunk_dto import ChunkDTO

class DocumentProcessorPort(ABC):
    """Output port for parsing files and splitting them into text chunks."""

    @abstractmethod
    def extract_and_chunk(self, file_path: str, mime_type: str) -> Sequence[ChunkDTO]:
        """Reads the file at file_path, extracts text, and chunks it."""
        pass
