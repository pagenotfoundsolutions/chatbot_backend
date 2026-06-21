import uuid
from typing import List, Optional
from sqlalchemy.orm import Session

from app.modules.ai_providers.application.ports.output.model_repository_port import ModelRepositoryPort
from app.modules.ai_providers.domain.entities.ai_model import AIModel
from app.modules.ai_providers.adapters.output.persistence.models.ai_model_model import AIModelModel
from app.modules.ai_providers.adapters.output.persistence.mapper import ModelMapper

class SqlAlchemyModelRepository(ModelRepositoryPort):
    def __init__(self, db_session: Session):
        self._db = db_session

    def save(self, entity: AIModel) -> None:
        model = ModelMapper.to_model(entity)
        self._db.merge(model)

    def get(self, id: uuid.UUID) -> Optional[AIModel]:
        model = self._db.query(AIModelModel).filter(AIModelModel.id == id, AIModelModel.deleted_at.is_(None)).first()
        return ModelMapper.to_domain(model) if model else None

    def delete(self, id: uuid.UUID) -> None:
        from datetime import datetime
        model = self._db.query(AIModelModel).filter(AIModelModel.id == id).first()
        if model:
            model.deleted_at = datetime.utcnow()

    def get_all_models(self) -> List[AIModel]:
        models = self._db.query(AIModelModel).filter(AIModelModel.deleted_at.is_(None)).all()
        return [ModelMapper.to_domain(m) for m in models]

    def get_models_by_provider(self, provider_id: uuid.UUID) -> List[AIModel]:
        models = self._db.query(AIModelModel).filter(AIModelModel.provider_id == provider_id, AIModelModel.deleted_at.is_(None)).all()
        return [ModelMapper.to_domain(m) for m in models]

    def get_active_models(self) -> List[AIModel]:
        models = self._db.query(AIModelModel).filter(AIModelModel.is_active == True, AIModelModel.deleted_at.is_(None)).all()
        return [ModelMapper.to_domain(m) for m in models]

    def get_active_models_by_provider(self, provider_id: uuid.UUID) -> List[AIModel]:
        models = self._db.query(AIModelModel).filter(
            AIModelModel.provider_id == provider_id, 
            AIModelModel.is_active == True,
            AIModelModel.deleted_at.is_(None)
        ).all()
        return [ModelMapper.to_domain(m) for m in models]

    def update_model_status(self, model_id: uuid.UUID, is_active: bool) -> None:
        model = self._db.query(AIModelModel).filter(AIModelModel.id == model_id).first()
        if model:
            model.is_active = is_active
            self._db.commit()
