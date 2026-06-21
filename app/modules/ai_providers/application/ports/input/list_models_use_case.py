from abc import ABC, abstractmethod
from typing import List

from app.modules.ai_providers.domain.entities.ai_model import AIModel

class ListModelsUseCase(ABC):
    @abstractmethod
    def execute(self) -> List[AIModel]:
        pass
