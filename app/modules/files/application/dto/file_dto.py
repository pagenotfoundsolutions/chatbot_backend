from dataclasses import dataclass
from datetime import datetime
import uuid

from app.modules.files.domain.entities.file import File
from app.modules.files.domain.enums.file_status import FileStatus


@dataclass(frozen=True)
class FileDTO:
    id: uuid.UUID
    auth_user_id: uuid.UUID
    original_filename: str
    mime_type: str
    size_bytes: int
    status: FileStatus
    error_message: str | None
    created_at: datetime
    updated_at: datetime
    storage_path: str

    @classmethod
    def from_entity(cls, entity: File) -> "FileDTO":
        return cls(
            id=entity.id,
            auth_user_id=entity.auth_user_id,
            original_filename=entity.original_filename,
            mime_type=entity.mime_type,
            size_bytes=entity.size_bytes,
            status=entity.status,
            error_message=entity.error_message,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            storage_path=entity.storage_path,
        )
