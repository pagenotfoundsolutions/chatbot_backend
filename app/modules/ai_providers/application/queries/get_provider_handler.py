import uuid
from typing import Optional

from app.modules.ai_providers.application.ports.input.get_provider_use_case import GetProviderUseCase
from app.modules.ai_providers.application.ports.output.provider_repository_port import ProviderRepositoryPort
from app.modules.ai_providers.domain.entities.ai_provider import AIProvider

class GetProviderHandler(GetProviderUseCase):
    def __init__(self, repository: ProviderRepositoryPort):
        self.repository = repository

    def execute(self, provider_id: uuid.UUID) -> Optional[AIProvider]:
        return self.repository.get(provider_id)
