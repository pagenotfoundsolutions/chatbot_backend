from typing import Sequence, Optional
import uuid

from sqlalchemy import select, delete, func
from sqlalchemy.orm import Session

from app.modules.rag.application.ports.output.vector_store_port import VectorStorePort
from app.modules.rag.domain.entities.document_chunk import DocumentChunk
from app.modules.rag.adapters.output.persistence.models.document_chunk_model import DocumentChunkModel

class SqlAlchemyVectorStoreRepository(VectorStorePort):
    def __init__(self, db: Session):
        self._db = db

    def save_chunks(self, chunks: Sequence[DocumentChunk]) -> None:
        if not chunks:
            return
            
        models = [
            DocumentChunkModel(
                id=chunk.id,
                file_id=chunk.file_id,
                auth_user_id=chunk.auth_user_id,
                content=chunk.content,
                page_number=chunk.page_number,
                chunk_index=chunk.chunk_index,
                embedding=chunk.embedding,
                content_tsvector=func.to_tsvector('english', chunk.content)
            ) for chunk in chunks
        ]
        
        self._db.add_all(models)
        self._db.flush()

    def search_similar(
        self, 
        query_embedding: list[float], 
        top_k: int = 5, 
        auth_user_id: Optional[uuid.UUID] = None,
        file_id: Optional[uuid.UUID] = None,
        query_text: Optional[str] = None
    ) -> Sequence[DocumentChunk]:
        
        # 1. Base query for Dense Vector Search
        vector_stmt = select(DocumentChunkModel.id)
        if auth_user_id:
            vector_stmt = vector_stmt.filter(DocumentChunkModel.auth_user_id == auth_user_id)
        if file_id:
            vector_stmt = vector_stmt.filter(DocumentChunkModel.file_id == file_id)
            
        vector_stmt = vector_stmt.order_by(DocumentChunkModel.embedding.l2_distance(query_embedding)).limit(20)
        vector_results = self._db.scalars(vector_stmt).all()
        
        # 2. Base query for Keyword Search (if query_text provided)
        keyword_results = []
        if query_text:
            keyword_stmt = select(DocumentChunkModel.id)
            if auth_user_id:
                keyword_stmt = keyword_stmt.filter(DocumentChunkModel.auth_user_id == auth_user_id)
            if file_id:
                keyword_stmt = keyword_stmt.filter(DocumentChunkModel.file_id == file_id)
                
            tsquery = func.plainto_tsquery('english', query_text)
            keyword_stmt = keyword_stmt.filter(DocumentChunkModel.content_tsvector.op('@@')(tsquery))
            keyword_stmt = keyword_stmt.order_by(func.ts_rank_cd(DocumentChunkModel.content_tsvector, tsquery).desc()).limit(20)
            keyword_results = self._db.scalars(keyword_stmt).all()
        
        # 3. Reciprocal Rank Fusion (RRF) in Python
        # Default K constant for RRF is typically 60
        RRF_K = 60
        scores = {}
        
        for rank, chunk_id in enumerate(vector_results, 1):
            scores[chunk_id] = scores.get(chunk_id, 0.0) + 1.0 / (RRF_K + rank)
            
        for rank, chunk_id in enumerate(keyword_results, 1):
            scores[chunk_id] = scores.get(chunk_id, 0.0) + 1.0 / (RRF_K + rank)
            
        # Sort by RRF score descending
        fused_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)[:top_k]
        
        if not fused_ids:
            return []
            
        # 4. Fetch the final models preserving order
        fetch_stmt = select(DocumentChunkModel).where(DocumentChunkModel.id.in_(fused_ids))
        models = self._db.scalars(fetch_stmt).all()
        
        # Map models back by id to preserve RRF sort order
        model_map = {m.id: m for m in models}
        ordered_models = [model_map[cid] for cid in fused_ids if cid in model_map]
        
        return [
            DocumentChunk(
                id=model.id,
                file_id=model.file_id,
                auth_user_id=model.auth_user_id,
                content=model.content,
                page_number=model.page_number,
                chunk_index=model.chunk_index,
                embedding=None
            ) for model in ordered_models
        ]

    def delete_by_file_id(self, file_id: uuid.UUID) -> None:
        stmt = delete(DocumentChunkModel).where(DocumentChunkModel.file_id == file_id)
        self._db.execute(stmt)
        self._db.flush()
