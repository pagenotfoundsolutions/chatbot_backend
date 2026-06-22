
from abc import ABC, abstractmethod
from app.modules.ai_providers.domain.entities.ai_provider import AIProvider
from typing import List
class ListProvidersWithActiveModelsUseCase(ABC):
    @abstractmethod
    def execute(self) -> List[AIProvider]:
        pass