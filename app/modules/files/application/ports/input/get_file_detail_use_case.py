from abc import ABC, abstractmethod
import uuid
from pydantic import BaseModel

from app.modules.files.application.dto.file_dto import FileDTO


class GetFileDetailQuery(BaseModel):
    auth_user_id: uuid.UUID
    file_id: uuid.UUID


class GetFileDetailUseCase(ABC):
    @abstractmethod
    def execute(self, query: GetFileDetailQuery) -> FileDTO:
        ...
