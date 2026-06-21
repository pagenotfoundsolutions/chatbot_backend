import uuid

from app.modules.ai_providers.application.ports.output.model_repository_port import ModelRepositoryPort
from app.modules.ai_providers.application.ports.input.delete_model_use_case import DeleteModelUseCase, DeleteModelCommand

class DeleteModelHandler(DeleteModelUseCase):
    def __init__(self, model_repo: ModelRepositoryPort):
        self._model_repo = model_repo

    def execute(self, command: DeleteModelCommand) -> bool:
        model = self._model_repo.get(command.id)
        if not model:
            return False
            
        self._model_repo.delete(command.id)
        return True
