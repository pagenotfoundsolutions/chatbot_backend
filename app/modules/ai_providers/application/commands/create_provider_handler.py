
from app.modules.ai_providers.domain.entities.ai_provider import AIProvider
from app.modules.ai_providers.application.ports.output.provider_repository_port import ProviderRepositoryPort
from app.modules.ai_providers.application.ports.input.create_provider_use_case import CreateProviderUseCase, CreateProviderCommand

class CreateProviderHandler(CreateProviderUseCase):
    def __init__(self, provider_repo: ProviderRepositoryPort):
        self._provider_repo = provider_repo

    def execute(self, command: CreateProviderCommand) -> AIProvider:
        # Check if a provider with this name already exists
        # Although unique constraint handles this at DB level, it's good to check or let it throw
        
        provider = AIProvider.create(
            name=command.name,
            display_name=command.display_name,
            description=command.description or "",
            api_base_url=command.api_base_url,
            api_key=command.api_key
        )
        
        self._provider_repo.save(provider)
        return provider
