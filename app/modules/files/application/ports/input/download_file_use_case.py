from abc import ABC, abstractmethod
import uuid
from typing import Any
from pydantic import BaseModel

from app.modules.files.application.dto.file_dto import FileDTO

class DownloadFileQuery(BaseModel):
    auth_user_id: uuid.UUID
    file_path: str

class DownloadFileResult(BaseModel):
    file_dto: FileDTO
    stream: Any

    model_config = {
        "arbitrary_types_allowed": True
    }

class DownloadFileUseCase(ABC):
    @abstractmethod
    def execute(self, query: DownloadFileQuery) -> DownloadFileResult:
        ...
