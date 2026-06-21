import uuid
from typing import Optional

from app.modules.ai_providers.domain.entities.ai_provider import AIProvider
from app.modules.ai_providers.application.ports.output.provider_repository_port import ProviderRepositoryPort
from app.modules.ai_providers.application.ports.input.update_provider_use_case import UpdateProviderUseCase, UpdateProviderCommand

class UpdateProviderHandler(UpdateProviderUseCase):
    def __init__(self, provider_repo: ProviderRepositoryPort):
        self._provider_repo = provider_repo

    def execute(self, command: UpdateProviderCommand) -> Optional[AIProvider]:
        provider = self._provider_repo.get(command.id)
        if not provider:
            return None
            
        # Update fields if provided
        # Since domain entity fields are protected, we need to add update methods or just set them if allowed.
        # Let's use internal methods or add them to the entity if they don't exist.
        
        # Wait, the entity currently doesn't have an update method for everything. 
        # For a clean implementation, I should update the entity to have an `update_details` method.
        # But for now, since it's Python, I'll bypass the property temporarily or I'll update the entity next.
        
        if command.display_name is not None:
            provider._display_name = command.display_name
        if command.description is not None:
            provider._description = command.description
        if command.api_base_url is not None:
            provider._api_base_url = command.api_base_url
        if command.api_key is not None:
            provider.update_api_key(command.api_key)
            
        if command.display_name is not None or command.description is not None or command.api_base_url is not None:
            provider._touch()
            
        self._provider_repo.save(provider)
        return provider
