import uuid
from abc import abstractmethod
from typing import Optional, List

from app.shared.kernel.base_repository import BaseRepository
from app.modules.ai_providers.domain.entities.ai_model import AIModel

class ModelRepositoryPort(BaseRepository[AIModel, uuid.UUID]):
    """
    Interface for saving and retrieving AI Models independently.
    """

    @abstractmethod
    def get_all_models(self) -> List[AIModel]:
        """
        Returns a list of all models across all providers.
        """
        pass

    @abstractmethod
    def get_models_by_provider(self, provider_id: uuid.UUID) -> List[AIModel]:
        """
        Returns a list of models belonging to a specific provider.
        """
        pass

    @abstractmethod
    def get_active_models(self) -> List[AIModel]:
        """
        Returns a list of all active models across all providers.
        """
        pass

    @abstractmethod
    def get_active_models_by_provider(self, provider_id: uuid.UUID) -> List[AIModel]:
        """
        Returns a list of active models belonging to a specific provider.
        """
        pass

    @abstractmethod
    def update_model_status(self, model_id: uuid.UUID, is_active: bool) -> None:
        """
        Updates the active/inactive status of a model directly.
        """
        pass

