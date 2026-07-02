from abc import ABC, abstractmethod
import uuid
from typing import Optional

from app.modules.files.domain.entities.file import File
from app.shared.kernel.base_repository import BaseRepository

class FileRepositoryPort(BaseRepository[File, uuid.UUID], ABC):
    """Outbound port for persisting the File aggregate."""

    @abstractmethod
    def get_by_user_and_hash(self, auth_user_id: uuid.UUID, file_hash: str) -> Optional[File]:
        """Check if a file with this content hash already exists for this user."""
        ...

    @abstractmethod
    def get_by_storage_path(self, storage_path: str) -> Optional[File]:
        """Get file by its storage path."""
        ...

    @abstractmethod
    def list_by_user(self, auth_user_id: uuid.UUID, page: int, size: int) -> tuple[list[File], int]:
        ...

    @abstractmethod
    def get_many_by_ids(self, ids: list[uuid.UUID]) -> list[File]:
        """Fetch multiple files by their IDs in a single query."""
        ...

    @abstractmethod
    def undelete(self, id: uuid.UUID) -> None:
        """Restore a soft-deleted file."""
        ...
