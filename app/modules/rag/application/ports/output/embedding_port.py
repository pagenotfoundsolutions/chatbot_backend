from abc import ABC, abstractmethod

class EmbeddingPort(ABC):
    """Output port for generating text embeddings."""

    @abstractmethod
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a list of documents/chunks."""
        pass

    @abstractmethod
    def embed_query(self, text: str) -> list[float]:
        """Generate an embedding for a single search query."""
        pass
