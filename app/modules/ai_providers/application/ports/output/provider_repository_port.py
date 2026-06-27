import uuid
from abc import abstractmethod
from typing import List

from app.shared.kernel.base_repository import BaseRepository
from app.modules.ai_providers.domain.entities.ai_provider import AIProvider

class ProviderRepositoryPort(BaseRepository[AIProvider, uuid.UUID]):
    """
    Interface for saving and retrieving AI Providers.
    """
    
    @abstractmethod
    def get_all_providers(self) -> List[AIProvider]:
        """
        Returns a list of all AI providers.
        """
        pass
    
    @abstractmethod
    def get_all_providers_with_active_models(self) -> List[AIProvider]:
        """
        Returns a list of all AI providers with their active models.
        """
        pass