from sqlalchemy.orm import Session
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from app.shared.config.settings import settings

from app.modules.rag.application.ports.output.embedding_port import EmbeddingPort

class DynamicEmbeddingAdapter(EmbeddingPort):
    def __init__(self, db: Session):
        self._db = db
        self.default_model_key = "nvidia/nv-embedcode-7b-v1"
        
        api_key = settings.nvidia_api_key
        if not api_key:
            import logging
            logging.getLogger(__name__).warning("NVIDIA_API_KEY is not set. Embeddings may fail.")
            
        self._embeddings = NVIDIAEmbeddings(
            model=self.default_model_key,
            api_key=api_key,
            truncate="NONE",
        )

    def _get_active_embeddings(self):
        return self._embeddings

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        embeddings_model = self._get_active_embeddings()
        return embeddings_model.embed_documents(texts)

    def embed_query(self, text: str) -> list[float]:
        embeddings_model = self._get_active_embeddings()
        return embeddings_model.embed_query(text)
