from typing import List

from app.modules.ai_providers.application.ports.input.list_providers_use_case import ListProvidersUseCase
from app.modules.ai_providers.application.ports.output.provider_repository_port import ProviderRepositoryPort
from app.modules.ai_providers.domain.entities.ai_provider import AIProvider

class ListProvidersHandler(ListProvidersUseCase):
    def __init__(self, repository: ProviderRepositoryPort):
        self.repository = repository

    def execute(self) -> List[AIProvider]:
        return self.repository.get_all_providers()
