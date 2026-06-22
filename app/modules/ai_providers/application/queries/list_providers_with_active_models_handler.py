

from app.modules.ai_providers.application.ports.input.list_providers_with_active_models_usecase import ListProvidersWithActiveModelsUseCase
from app.modules.ai_providers.domain.entities.ai_provider import AIProvider
from app.modules.ai_providers.application.ports.output.provider_repository_port import ProviderRepositoryPort
from typing import List
class ListProvidersWithActiveModelsHandler(ListProvidersWithActiveModelsUseCase):
    def __init__(self, repo: ProviderRepositoryPort):
        self._repo = repo

    def execute(self) -> List[AIProvider]:
        return self._repo.get_all_providers_with_active_models()