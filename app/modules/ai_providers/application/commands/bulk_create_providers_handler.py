from typing import List
from app.modules.ai_providers.application.ports.input.bulk_create_providers_use_case import BulkCreateProvidersUseCase, BulkCreateProvidersCommand

from app.modules.ai_providers.application.ports.input.create_provider_use_case import CreateProviderUseCase, CreateProviderCommand
from app.modules.ai_providers.application.ports.input.create_model_use_case import CreateModelUseCase, CreateModelCommand

class BulkCreateProvidersHandler(BulkCreateProvidersUseCase):
    def __init__(self, create_provider_use_case: CreateProviderUseCase, create_model_use_case: CreateModelUseCase):
        self._create_provider_use_case = create_provider_use_case
        self._create_model_use_case = create_model_use_case

    def execute(self, command: BulkCreateProvidersCommand) -> None:
        for item in command.items:
            # Create the provider
            provider_cmd = CreateProviderCommand(**item.provider)
            provider = self._create_provider_use_case.execute(provider_cmd)
            
            # Create associated models
            for model_dict in item.models:
                # Assign the newly created provider's ID to the model payload
                model_dict["provider_id"] = provider.id
                model_cmd = CreateModelCommand(**model_dict)
                self._create_model_use_case.execute(model_cmd)
