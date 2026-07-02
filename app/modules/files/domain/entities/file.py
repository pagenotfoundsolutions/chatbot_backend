from __future__ import annotations
import uuid
from datetime import datetime

from app.shared.kernel.aggregate_root import AggregateRoot
from app.shared.kernel.utils import generate_uuid, utc_now
from app.modules.files.domain.enums.file_status import FileStatus


class File(AggregateRoot[uuid.UUID]):
    """Aggregate root for an uploaded file."""

    def __init__(
        self,
        id: uuid.UUID,
        auth_user_id: uuid.UUID,
        original_filename: str,
        stored_filename: str,
        mime_type: str,
        size_bytes: int,
        storage_path: str,
        file_hash: str,
        status: FileStatus,
        error_message: str | None,
        created_at: datetime,
        updated_at: datetime,
        is_deleted: bool = False,
    ) -> None:
        super().__init__(id)
        self._auth_user_id = auth_user_id
        self._original_filename = original_filename
        self._stored_filename = stored_filename
        self._mime_type = mime_type
        self._size_bytes = size_bytes
        self._storage_path = storage_path
        self._file_hash = file_hash
        self._status = status
        self._error_message = error_message
        self._created_at = created_at
        self._updated_at = updated_at
        self._is_deleted = is_deleted

    @classmethod
    def create(
        cls,
        auth_user_id: uuid.UUID,
        original_filename: str,
        stored_filename: str,
        mime_type: str,
        size_bytes: int,
        storage_path: str,
        file_hash: str,
    ) -> "File":
        """Start a new file entity."""
        now = utc_now()
        return cls(
            id=generate_uuid(),
            auth_user_id=auth_user_id,
            original_filename=original_filename,
            stored_filename=stored_filename,
            mime_type=mime_type,
            size_bytes=size_bytes,
            storage_path=storage_path,
            file_hash=file_hash,
            status=FileStatus.PENDING,
            error_message=None,
            created_at=now,
            updated_at=now,
        )

    # --- read-only properties ---

    @property
    def auth_user_id(self) -> uuid.UUID:
        return self._auth_user_id

    @property
    def original_filename(self) -> str:
        return self._original_filename

    @property
    def stored_filename(self) -> str:
        return self._stored_filename

    @property
    def mime_type(self) -> str:
        return self._mime_type

    @property
    def size_bytes(self) -> int:
        return self._size_bytes

    @property
    def storage_path(self) -> str:
        return self._storage_path

    @property
    def file_hash(self) -> str:
        return self._file_hash

    @property
    def status(self) -> FileStatus:
        return self._status

    @property
    def error_message(self) -> str | None:
        return self._error_message

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @property
    def is_deleted(self) -> bool:
        return self._is_deleted

    # --- behaviors ---
    
    def mark_as_processing(self) -> None:
        if self._status not in [FileStatus.PENDING, FileStatus.ERROR]:
            raise ValueError(f"Cannot process file in status {self._status}")
        self._status = FileStatus.PROCESSING
        self._touch()
        
    def mark_as_parsed(self) -> None:
        if self._status != FileStatus.PROCESSING:
            raise ValueError(f"Cannot mark as parsed from status {self._status}")
        self._status = FileStatus.PARSED
        self._error_message = None
        self._touch()
        
    def mark_as_error(self, message: str) -> None:
        self._status = FileStatus.ERROR
        self._error_message = message
        self._touch()

    def _touch(self) -> None:
        self._updated_at = utc_now()
