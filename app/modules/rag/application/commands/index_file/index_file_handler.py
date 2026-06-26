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
        # 1. Fetch file entity
        file_entity = self.file_repo.get_by_id(command.file_id)
        if not file_entity:
            raise ValueError(f"File {command.file_id} not found.")

        if file_entity.auth_user_id != command.auth_user_id:
            raise PermissionError("User does not have permission to index this file.")

        # Resolve actual file path
        base_dir = os.path.join(settings.storage_path) if hasattr(settings, "storage_path") else "storage"
        file_path = os.path.join(base_dir, file_entity.storage_path)
        if not os.path.exists(file_path):
            file_path = file_entity.storage_path 

        # 2. Extract and chunk text using the processor port
        chunks_dto = self.document_processor.extract_and_chunk(file_path, file_entity.mime_type)
        if not chunks_dto:
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
            self.vector_store.save_chunks(chunks)

