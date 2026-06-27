from sqlalchemy.orm import Session
from langchain_huggingface import HuggingFaceEndpointEmbeddings

from app.modules.rag.application.ports.output.embedding_port import EmbeddingPort

class DynamicEmbeddingAdapter(EmbeddingPort):
    def __init__(self, db: Session):
        self._db = db
        self.default_model_key = "text-embedding-3-small"
        # Uses HuggingFace Inference API via API key, NO local models!
        self._fallback_embeddings = HuggingFaceEndpointEmbeddings(
            model="sentence-transformers/all-MiniLM-L6-v2",
            task="feature-extraction"
        )

    def _get_active_embeddings(self):
        # Using free HuggingFace API embeddings instead of OpenAI
        return self._fallback_embeddings

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        embeddings_model = self._get_active_embeddings()
        return embeddings_model.embed_documents(texts)

    def embed_query(self, text: str) -> list[float]:
        embeddings_model = self._get_active_embeddings()
        return embeddings_model.embed_query(text)
