import uuid

from app.modules.ai_providers.application.ports.input.get_provider_config_use_case import GetProviderConfigUseCase
from app.modules.ai_providers.application.dto.provider_config_dto import ProviderConfigDTO
from app.modules.ai_providers.application.ports.output.provider_repository_port import ProviderRepositoryPort
from app.modules.ai_providers.application.ports.output.model_repository_port import ModelRepositoryPort

class GetProviderConfigHandler(GetProviderConfigUseCase):
    """Handles fetching and assembling the ProviderConfigDTO."""
    
    def __init__(
        self, 
        provider_repo: ProviderRepositoryPort, 
        model_repo: ModelRepositoryPort
    ) -> None:
        self._provider_repo = provider_repo
        self._model_repo = model_repo

    def execute(self, provider_id: uuid.UUID, model_id: uuid.UUID) -> ProviderConfigDTO | None:
        provider = self._provider_repo.get(provider_id)
        if not provider:
            return None
            
        model = self._model_repo.get(model_id)
        if not model or not model.is_active:
            return None
            
        if model.provider_id != provider.id:
            return None

        return ProviderConfigDTO(
            provider_name=provider.name.lower(),
            model_key=model.model_key,
            api_key=provider.api_key,
            base_url=provider.api_base_url if provider.api_base_url else None
        )
