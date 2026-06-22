from app.modules.ai_providers.application.ports.input.list_providers_with_active_models_usecase import ListProvidersWithActiveModelsUseCase
from app.modules.ai_providers.application.queries.list_providers_with_active_models_handler import ListProvidersWithActiveModelsHandler
from fastapi import Depends
from sqlalchemy.orm import Session

from app.shared.database.session import get_db

from app.modules.ai_providers.application.ports.output.provider_repository_port import ProviderRepositoryPort
from app.modules.ai_providers.application.ports.output.model_repository_port import ModelRepositoryPort
from app.modules.ai_providers.adapters.output.persistence.sqlalchemy_provider_repository import SqlAlchemyProviderRepository
from app.modules.ai_providers.adapters.output.persistence.sqlalchemy_model_repository import SqlAlchemyModelRepository

from app.modules.ai_providers.application.ports.input.list_providers_use_case import ListProvidersUseCase
from app.modules.ai_providers.application.ports.input.get_provider_use_case import GetProviderUseCase
from app.modules.ai_providers.application.ports.input.list_models_use_case import ListModelsUseCase
from app.modules.ai_providers.application.ports.input.list_active_models_use_case import ListActiveModelsUseCase
from app.modules.ai_providers.application.ports.input.get_model_use_case import GetModelUseCase

from app.modules.ai_providers.application.queries.list_providers_handler import ListProvidersHandler
from app.modules.ai_providers.application.queries.get_provider_handler import GetProviderHandler
from app.modules.ai_providers.application.queries.list_models_handler import ListModelsHandler
from app.modules.ai_providers.application.queries.list_active_models_handler import ListActiveModelsHandler
from app.modules.ai_providers.application.queries.get_model_handler import GetModelHandler

def get_provider_repository(db: Session = Depends(get_db)) -> ProviderRepositoryPort:
    return SqlAlchemyProviderRepository(db)

def get_model_repository(db: Session = Depends(get_db)) -> ModelRepositoryPort:
    return SqlAlchemyModelRepository(db)


def get_list_providers_use_case(
    repository: ProviderRepositoryPort = Depends(get_provider_repository),
) -> ListProvidersUseCase:
    return ListProvidersHandler(repository)

def get_get_provider_use_case(
    repository: ProviderRepositoryPort = Depends(get_provider_repository),
) -> GetProviderUseCase:
    return GetProviderHandler(repository)


def get_list_models_use_case(
    repository: ModelRepositoryPort = Depends(get_model_repository),
) -> ListModelsUseCase:
    return ListModelsHandler(repository)

def get_list_active_models_use_case(
    repository: ModelRepositoryPort = Depends(get_model_repository),
) -> ListActiveModelsUseCase:
    return ListActiveModelsHandler(repository)

def get_get_model_use_case(
    repository: ModelRepositoryPort = Depends(get_model_repository),
) -> GetModelUseCase:
    return GetModelHandler(repository)

def get_list_providers_with_active_models_use_case(
    repository: ProviderRepositoryPort = Depends(get_provider_repository),
) -> ListProvidersWithActiveModelsUseCase:
    return ListProvidersWithActiveModelsHandler(repository)