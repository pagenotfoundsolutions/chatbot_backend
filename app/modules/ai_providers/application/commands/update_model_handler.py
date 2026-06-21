import uuid
from typing import Optional, Dict, Any

from app.modules.ai_providers.domain.entities.ai_model import AIModel
from app.modules.ai_providers.application.ports.output.model_repository_port import ModelRepositoryPort
from app.modules.ai_providers.application.ports.input.update_model_use_case import UpdateModelUseCase, UpdateModelCommand

class UpdateModelHandler(UpdateModelUseCase):
    def __init__(self, model_repo: ModelRepositoryPort):
        self._model_repo = model_repo

    def execute(self, command: UpdateModelCommand) -> Optional[AIModel]:
        model = self._model_repo.get(command.id)
        if not model:
            return None
            
        changed = False
        
        for attr, value in vars(command).items():
            if attr == "id" or value is None:
                continue
            
            # Use the internal attribute name for the entity
            internal_attr = f"_{attr}"
            if hasattr(model, internal_attr):
                setattr(model, internal_attr, value)
                changed = True
                
        if changed:
            model._touch()
            self._model_repo.save(model)
            
        return model
