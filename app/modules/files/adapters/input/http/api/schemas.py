import uuid
from datetime import datetime
from pydantic import BaseModel

from app.modules.files.domain.enums.file_status import FileStatus


class FileResponse(BaseModel):
    id: uuid.UUID
    auth_user_id: uuid.UUID
    original_filename: str
    mime_type: str
    size_bytes: int
    status: FileStatus
    error_message: str | None
    created_at: datetime
    updated_at: datetime
    file_path: str
