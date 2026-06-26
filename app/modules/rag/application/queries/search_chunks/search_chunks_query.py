import uuid
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class SearchChunksQuery:
    """Query to search for document chunks."""
    text: str
    auth_user_id: uuid.UUID
    top_k: int = 5
    file_id: Optional[uuid.UUID] = None
