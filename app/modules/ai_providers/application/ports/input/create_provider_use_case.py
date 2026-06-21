from typing import Optional
from abc import ABC, abstractmethod
from app.modules.ai_providers.domain.entities.ai_provider import AIProvider

class CreateProviderCommand:
    def __init__(self, name: str, display_name: str, description: Optional[str], api_base_url: str, api_key: str):
        self.name = name
        self.display_name = display_name
        self.description = description
        self.api_base_url = api_base_url
        self.api_key = api_key

class CreateProviderUseCase(ABC):
    @abstractmethod
    def execute(self, command: CreateProviderCommand) -> AIProvider:
        pass
