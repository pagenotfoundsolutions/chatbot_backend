from fastapi import Depends
from sqlalchemy.orm import Session

from app.shared.database.session import get_db
from app.modules.files.adapters.input.http.api.dependencies import get_file_repository
from app.modules.rag.adapters.output.persistence.sqlalchemy_vector_store_repository import SqlAlchemyVectorStoreRepository
from app.modules.rag.adapters.output.embeddings.dynamic_embedding_adapter import DynamicEmbeddingAdapter
from app.modules.rag.adapters.output.document_processor.langchain_document_processor_adapter import LangchainDocumentProcessorAdapter
from app.modules.rag.application.commands.index_file.index_file_handler import IndexFileHandler
from app.modules.rag.application.queries.search_chunks.search_chunks_handler import SearchChunksHandler

def get_embedding_port(db: Session = Depends(get_db)) -> DynamicEmbeddingAdapter:
    return DynamicEmbeddingAdapter(db=db)

def get_vector_store_port(db: Session = Depends(get_db)) -> SqlAlchemyVectorStoreRepository:
    return SqlAlchemyVectorStoreRepository(db=db)

def get_document_processor_port() -> LangchainDocumentProcessorAdapter:
    return LangchainDocumentProcessorAdapter()

def get_index_file_use_case(
    file_repo = Depends(get_file_repository),
    vector_store = Depends(get_vector_store_port),
    embedding_port = Depends(get_embedding_port),
    document_processor = Depends(get_document_processor_port)
) -> IndexFileHandler:
    return IndexFileHandler(
        file_repo=file_repo, 
        vector_store=vector_store,
        embedding_port=embedding_port,
        document_processor=document_processor
    )

def get_search_chunks_use_case(
    vector_store = Depends(get_vector_store_port),
    embedding_port = Depends(get_embedding_port)
) -> SearchChunksHandler:
    return SearchChunksHandler(
        vector_store=vector_store, 
        embedding_port=embedding_port
    )
