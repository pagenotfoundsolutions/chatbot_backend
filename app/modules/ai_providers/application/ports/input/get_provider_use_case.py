import uuid
from abc import ABC, abstractmethod
from typing import Optional

from app.modules.ai_providers.domain.entities.ai_provider import AIProvider

class GetProviderUseCase(ABC):
    @abstractmethod
    def execute(self, provider_id: uuid.UUID) -> Optional[AIProvider]:
        pass
