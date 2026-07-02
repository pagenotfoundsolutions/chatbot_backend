from abc import ABC, abstractmethod
from dataclasses import dataclass
import uuid


@dataclass(frozen=True)
class DeleteFileCommand:
    auth_user_id: uuid.UUID
    file_id: uuid.UUID


class DeleteFileUseCase(ABC):
    @abstractmethod
    def execute(self, command: DeleteFileCommand) -> None:
        ...
