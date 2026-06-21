from fastapi import Depends
from sqlalchemy.orm import Session

from app.shared.database.session import get_db

from app.modules.ai_providers.application.ports.output.provider_repository_port import ProviderRepositoryPort
from app.modules.ai_providers.application.ports.output.model_repository_port import ModelRepositoryPort
from app.modules.ai_providers.adapters.output.persistence.sqlalchemy_provider_repository import SqlAlchemyProviderRepository
from app.modules.ai_providers.adapters.output.persistence.sqlalchemy_model_repository import SqlAlchemyModelRepository

from app.modules.ai_providers.application.ports.input.create_provider_use_case import CreateProviderUseCase
from app.modules.ai_providers.application.commands.create_provider_handler import CreateProviderHandler
from app.modules.ai_providers.application.ports.input.update_provider_use_case import UpdateProviderUseCase
from app.modules.ai_providers.application.commands.update_provider_handler import UpdateProviderHandler
from app.modules.ai_providers.application.ports.input.delete_provider_use_case import DeleteProviderUseCase
from app.modules.ai_providers.application.commands.delete_provider_handler import DeleteProviderHandler

from app.modules.ai_providers.application.ports.input.create_model_use_case import CreateModelUseCase
from app.modules.ai_providers.application.commands.create_model_handler import CreateModelHandler
from app.modules.ai_providers.application.ports.input.update_model_use_case import UpdateModelUseCase
from app.modules.ai_providers.application.commands.update_model_handler import UpdateModelHandler
from app.modules.ai_providers.application.ports.input.delete_model_use_case import DeleteModelUseCase
from app.modules.ai_providers.application.commands.delete_model_handler import DeleteModelHandler

# Re-use the repositories directly or import from api.dependencies
from app.modules.ai_providers.adapters.input.http.api.dependencies import get_provider_repository, get_model_repository

def get_create_provider_use_case(repository: ProviderRepositoryPort = Depends(get_provider_repository)) -> CreateProviderUseCase:
    return CreateProviderHandler(repository)

def get_update_provider_use_case(repository: ProviderRepositoryPort = Depends(get_provider_repository)) -> UpdateProviderUseCase:
    return UpdateProviderHandler(repository)

def get_delete_provider_use_case(repository: ProviderRepositoryPort = Depends(get_provider_repository)) -> DeleteProviderUseCase:
    return DeleteProviderHandler(repository)

def get_create_model_use_case(repository: ModelRepositoryPort = Depends(get_model_repository)) -> CreateModelUseCase:
    return CreateModelHandler(repository)

def get_update_model_use_case(repository: ModelRepositoryPort = Depends(get_model_repository)) -> UpdateModelUseCase:
    return UpdateModelHandler(repository)

def get_delete_model_use_case(repository: ModelRepositoryPort = Depends(get_model_repository)) -> DeleteModelUseCase:
    return DeleteModelHandler(repository)


