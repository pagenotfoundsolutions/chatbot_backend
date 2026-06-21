from typing import List

from app.modules.ai_providers.application.ports.input.list_active_models_use_case import ListActiveModelsUseCase
from app.modules.ai_providers.application.ports.output.model_repository_port import ModelRepositoryPort
from app.modules.ai_providers.domain.entities.ai_model import AIModel

class ListActiveModelsHandler(ListActiveModelsUseCase):
    def __init__(self, repository: ModelRepositoryPort):
        self.repository = repository

    def execute(self) -> List[AIModel]:
        return self.repository.get_active_models()
