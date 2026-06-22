from app.modules.ai_providers.adapters.output.persistence.models.ai_model_model import AIModelModel
import uuid
from typing import List, Optional
from sqlalchemy.orm import Session

from app.modules.ai_providers.application.ports.output.provider_repository_port import ProviderRepositoryPort
from app.modules.ai_providers.domain.entities.ai_provider import AIProvider
from app.modules.ai_providers.adapters.output.persistence.models.ai_provider_model import AIProviderModel
from app.modules.ai_providers.adapters.output.persistence.mapper import ProviderMapper

class SqlAlchemyProviderRepository(ProviderRepositoryPort):
    def __init__(self, db_session: Session):
        self._db = db_session

    def save(self, entity: AIProvider) -> None:
        model = ProviderMapper.to_model(entity)
        self._db.merge(model)

    def get(self, id: uuid.UUID) -> Optional[AIProvider]:
        model = self._db.query(AIProviderModel).filter(AIProviderModel.id == id).first()
        return ProviderMapper.to_domain(model) if model else None

    def delete(self, id: uuid.UUID) -> None:
        model = self._db.query(AIProviderModel).filter(AIProviderModel.id == id).first()
        if model:
            self._db.delete(model)

    def get_all_providers(self) -> List[AIProvider]:
        models = self._db.query(AIProviderModel).all()
        return [ProviderMapper.to_domain(m) for m in models]
    
    def get_all_providers_with_active_models(self) -> List[AIProvider]:
        models = self._db.query(AIProviderModel).filter(AIProviderModel.models.any(AIModelModel.is_active == True)).all()
        return [ProviderMapper.to_domain(m) for m in models]
