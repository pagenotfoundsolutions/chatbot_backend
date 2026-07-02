import os
from app.modules.files.application.ports.output.file_repository_port import FileRepositoryPort
from app.modules.rag.application.ports.output.vector_store_port import VectorStorePort
from app.modules.rag.application.ports.output.embedding_port import EmbeddingPort
from app.modules.rag.application.commands.index_file.index_file_command import IndexFileCommand
from app.modules.rag.domain.entities.document_chunk import DocumentChunk
from app.shared.config.settings import settings

from app.modules.rag.application.ports.output.document_processor_port import DocumentProcessorPort

class IndexFileHandler:
    def __init__(
        self, 
        file_repo: FileRepositoryPort, 
        vector_store: VectorStorePort,
        embedding_port: EmbeddingPort,
        document_processor: DocumentProcessorPort
    ):
        self.file_repo = file_repo
        self.vector_store = vector_store
        self.embedding_port = embedding_port
        self.document_processor = document_processor

    def execute(self, command: IndexFileCommand) -> None:
        from app.shared.database.database import SessionLocal
        from app.modules.files.adapters.output.persistence.sqlalchemy_file_repository import SqlAlchemyFileRepository
        
        # Create a fresh session for the background task
        with SessionLocal() as db:
            # We recreate the file repo with the fresh session
            fresh_file_repo = SqlAlchemyFileRepository(session=db)
            
            # 1. Fetch file entity using fresh repo
            file_entity = fresh_file_repo.get(command.file_id)
            if not file_entity:
                raise ValueError(f"File {command.file_id} not found.")
            if file_entity.auth_user_id != command.auth_user_id:
                raise ValueError("Unauthorized to index this file.")

            from app.modules.files.domain.enums.file_status import FileStatus
            try:
                # Mark as processing
                file_entity.mark_as_processing()
                fresh_file_repo.save(file_entity)
                
                # Resolve actual file path
                base_dir = settings.upload_dir if hasattr(settings, "upload_dir") else "storage/uploads"
                file_path = os.path.join(base_dir, file_entity.storage_path)
                if not os.path.exists(file_path):
                    file_path = file_entity.storage_path 

                # 2. Extract and chunk text using the processor port
                chunks_dto = self.document_processor.extract_and_chunk(file_path, file_entity.mime_type)
                if not chunks_dto:
                    file_entity.mark_as_parsed()
                    fresh_file_repo.save(file_entity)
                    return

                # 3. Generate Embeddings
                texts = [chunk.content for chunk in chunks_dto]
                embeddings = self.embedding_port.embed_documents(texts)

                # 4. Map to DocumentChunk entities
                chunks = []
                for i, chunk_dto in enumerate(chunks_dto):
                    chunk = DocumentChunk.create(
                        file_id=command.file_id,
                        auth_user_id=command.auth_user_id,
                        content=chunk_dto.content,
                        chunk_index=i,
                        page_number=chunk_dto.page_number,
                        embedding=embeddings[i] if i < len(embeddings) else None
                    )
                    chunks.append(chunk)

                # 5. Store in Vector DB
                if chunks:
                    # Idempotency: clear existing chunks for this file if any
                    self.vector_store.delete_by_file_id(command.file_id)
                    self.vector_store.save_chunks(chunks)
                    
                # Mark as successfully parsed
                file_entity.mark_as_parsed()
                fresh_file_repo.save(file_entity)
                
            except Exception as e:
                file_entity.mark_as_error(str(e))
                fresh_file_repo.save(file_entity)
                raise e

