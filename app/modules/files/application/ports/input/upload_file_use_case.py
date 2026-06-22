from abc import ABC, abstractmethod
from typing import BinaryIO
import uuid
from dataclasses import dataclass

from app.modules.files.application.dto.file_dto import FileDTO


@dataclass(frozen=True)
class UploadFileCommand:
    auth_user_id: uuid.UUID
    filename: str
    mime_type: str
    file_obj: BinaryIO


class UploadFileUseCase(ABC):
    """Driving port: upload a new file."""

    @abstractmethod
    def execute(self, command: UploadFileCommand) -> FileDTO:
        ...
