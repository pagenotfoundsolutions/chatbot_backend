import uuid
from abc import ABC, abstractmethod

class DeleteModelCommand:
    def __init__(self, id: uuid.UUID):
        self.id = id

class DeleteModelUseCase(ABC):
    @abstractmethod
    def execute(self, command: DeleteModelCommand) -> bool:
        pass
