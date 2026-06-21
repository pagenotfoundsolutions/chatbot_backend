import uuid
from typing import Optional
from abc import ABC, abstractmethod
from app.modules.ai_providers.domain.entities.ai_provider import AIProvider

class UpdateProviderCommand:
    def __init__(
        self, 
        id: uuid.UUID,
        display_name: Optional[str] = None, 
        description: Optional[str] = None, 
        api_base_url: Optional[str] = None, 
        api_key: Optional[str] = None
    ):
        self.id = id
        self.display_name = display_name
        self.description = description
        self.api_base_url = api_base_url
        self.api_key = api_key

class UpdateProviderUseCase(ABC):
    @abstractmethod
    def execute(self, command: UpdateProviderCommand) -> Optional[AIProvider]:
        pass
