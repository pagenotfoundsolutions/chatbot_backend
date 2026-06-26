from sqlalchemy.orm import Session
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

from app.modules.rag.application.ports.output.embedding_port import EmbeddingPort
from app.modules.ai_providers.adapters.output.persistence.models.ai_provider_model import AIProviderModel
from app.modules.ai_providers.adapters.output.persistence.models.ai_model_model import AIModelModel

class DynamicEmbeddingAdapter(EmbeddingPort):
    def __init__(self, db: Session):
        self._db = db
        self.default_model_key = "text-embedding-3-small"
        self._fallback_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    def _get_active_embeddings(self):
        # Using free HuggingFace embeddings instead of OpenAI
        return self._fallback_embeddings

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        embeddings_model = self._get_active_embeddings()
        return embeddings_model.embed_documents(texts)

    def embed_query(self, text: str) -> list[float]:
        embeddings_model = self._get_active_embeddings()
        return embeddings_model.embed_query(text)
