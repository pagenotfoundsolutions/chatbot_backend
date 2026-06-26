from typing import Sequence
import os

from app.modules.rag.application.ports.output.vector_store_port import VectorStorePort
from app.modules.rag.application.ports.output.embedding_port import EmbeddingPort
from app.modules.rag.application.queries.search_chunks.search_chunks_query import SearchChunksQuery
from app.modules.rag.application.ports.input.search_chunks_use_case import SearchChunksUseCase
from app.modules.rag.domain.entities.document_chunk import DocumentChunk
from flashrank import Ranker, RerankRequest

class SearchChunksHandler(SearchChunksUseCase):
    def __init__(
        self, 
        vector_store: VectorStorePort, 
        embedding_port: EmbeddingPort
    ):
        self.vector_store = vector_store
        self.embedding_port = embedding_port
        
        # Initialize lightweight ranker (loads ms-marco-TinyBERT ~15MB)
        # Using a shared temp cache dir to avoid re-downloads
        cache_dir = os.path.join(os.getcwd(), ".flashrank_cache")
        os.makedirs(cache_dir, exist_ok=True)
        self.ranker = Ranker(cache_dir=cache_dir)

    def execute(self, query: SearchChunksQuery) -> Sequence[DocumentChunk]:
        # 1. Embed the query
        query_embedding = self.embedding_port.embed_query(query.text)
        
        # 2. Hybrid Search (fetch more than top_k for reranking, e.g., 20)
        chunks = self.vector_store.search_similar(
            query_embedding=query_embedding,
            top_k=20,  # over-fetch for reranking
            auth_user_id=query.auth_user_id,
            file_id=query.file_id,
            query_text=query.text
        )
        
        if not chunks:
            return []

        # 3. Rerank the chunks using Flashrank Cross-Encoder
        passages = [
            {
                "id": str(chunk.id),
                "text": chunk.content,
                "meta": {"chunk_obj": chunk} # attach object to retrieve later
            }
            for chunk in chunks
        ]
        
        rerank_request = RerankRequest(query=query.text, passages=passages)
        ranked_results = self.ranker.rerank(rerank_request)
        
        # Extract the top_k chunks from the ranked results
        top_chunks = []
        for res in ranked_results[:query.top_k]:
            original_chunk = res["meta"]["chunk_obj"]
            top_chunks.append(original_chunk)
            
        return top_chunks
