import uuid
from abc import ABC, abstractmethod
from typing import Optional

from app.modules.ai_providers.domain.entities.ai_model import AIModel

class GetModelUseCase(ABC):
    @abstractmethod
    def execute(self, model_id: uuid.UUID) -> Optional[AIModel]:
        pass
