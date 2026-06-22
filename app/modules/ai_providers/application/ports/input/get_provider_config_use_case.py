import uuid
from abc import ABC, abstractmethod

from app.modules.ai_providers.application.dto.provider_config_dto import ProviderConfigDTO

class GetProviderConfigUseCase(ABC):
    """Application service (Input Port) exposed by the ai_providers module
    to allow other modules to securely fetch provider configurations without
    depending on the internal database structure.
    """
    
    @abstractmethod
    def execute(self, provider_id: uuid.UUID, model_id: uuid.UUID) -> ProviderConfigDTO | None:
        """Fetch the configuration. Returns None if provider/model is not found or is inactive."""
        pass
