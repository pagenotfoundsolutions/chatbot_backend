from abc import ABC, abstractmethod
from typing import List

from app.modules.ai_providers.domain.entities.ai_provider import AIProvider

class ListProvidersUseCase(ABC):
    @abstractmethod
    def execute(self) -> List[AIProvider]:
        pass
