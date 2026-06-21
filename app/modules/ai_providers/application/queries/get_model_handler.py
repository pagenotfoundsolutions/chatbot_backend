import uuid
from typing import Optional

from app.modules.ai_providers.application.ports.input.get_model_use_case import GetModelUseCase
from app.modules.ai_providers.application.ports.output.model_repository_port import ModelRepositoryPort
from app.modules.ai_providers.domain.entities.ai_model import AIModel

class GetModelHandler(GetModelUseCase):
    def __init__(self, repository: ModelRepositoryPort):
        self.repository = repository

    def execute(self, model_id: uuid.UUID) -> Optional[AIModel]:
        return self.repository.get(model_id)
