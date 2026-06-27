
from app.modules.ai_providers.application.ports.output.provider_repository_port import ProviderRepositoryPort
from app.modules.ai_providers.application.ports.input.delete_provider_use_case import DeleteProviderUseCase, DeleteProviderCommand

class DeleteProviderHandler(DeleteProviderUseCase):
    def __init__(self, provider_repo: ProviderRepositoryPort):
        self._provider_repo = provider_repo

    def execute(self, command: DeleteProviderCommand) -> bool:
        provider = self._provider_repo.get(command.id)
        if not provider:
            return False
            
        self._provider_repo.delete(command.id)
        return True
