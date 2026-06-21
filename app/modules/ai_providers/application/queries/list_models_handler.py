from typing import List

from app.modules.ai_providers.application.ports.input.list_models_use_case import ListModelsUseCase
from app.modules.ai_providers.application.ports.output.model_repository_port import ModelRepositoryPort
from app.modules.ai_providers.domain.entities.ai_model import AIModel

class ListModelsHandler(ListModelsUseCase):
    def __init__(self, repository: ModelRepositoryPort):
        self.repository = repository

    def execute(self) -> List[AIModel]:
        return self.repository.get_all_models()
