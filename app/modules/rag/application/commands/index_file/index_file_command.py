import uuid
from dataclasses import dataclass

@dataclass(frozen=True)
class IndexFileCommand:
    """Command to index a file into the RAG vector store."""
    file_id: uuid.UUID
    auth_user_id: uuid.UUID
