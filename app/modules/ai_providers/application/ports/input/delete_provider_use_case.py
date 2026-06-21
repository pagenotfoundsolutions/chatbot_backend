import uuid
from abc import ABC, abstractmethod

class DeleteProviderCommand:
    def __init__(self, id: uuid.UUID):
        self.id = id

class DeleteProviderUseCase(ABC):
    @abstractmethod
    def execute(self, command: DeleteProviderCommand) -> bool:
        pass
