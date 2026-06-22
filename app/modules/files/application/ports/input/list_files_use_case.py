from abc import ABC, abstractmethod
import uuid
from pydantic import BaseModel

from app.modules.files.application.dto.file_dto import FileDTO

from app.shared.pagination import Page

class ListFilesQuery(BaseModel):
    auth_user_id: uuid.UUID
    page: int = 1
    size: int = 50

class ListFilesUseCase(ABC):
    @abstractmethod
    def execute(self, query: ListFilesQuery) -> Page[FileDTO]:
        ...
