import uuid
from typing import Optional

from app.modules.ai_providers.adapters.input.http.api.schemas import AIProviderResponse, AIModelResponse
from app.modules.ai_providers.adapters.input.http.mappers.view_mapper import AIProvidersViewMapper
from app.modules.ai_providers.adapters.input.http.admin.schemas import CreateProviderRequest, UpdateProviderRequest, CreateModelRequest, UpdateModelRequest

from app.modules.ai_providers.application.ports.input.create_provider_use_case import CreateProviderUseCase, CreateProviderCommand
from app.modules.ai_providers.application.ports.input.update_provider_use_case import UpdateProviderUseCase, UpdateProviderCommand
from app.modules.ai_providers.application.ports.input.delete_provider_use_case import DeleteProviderUseCase, DeleteProviderCommand

from app.modules.ai_providers.application.ports.input.create_model_use_case import CreateModelUseCase, CreateModelCommand
from app.modules.ai_providers.application.ports.input.update_model_use_case import UpdateModelUseCase, UpdateModelCommand
from app.modules.ai_providers.application.ports.input.delete_model_use_case import DeleteModelUseCase, DeleteModelCommand

class AIProvidersAdminController:
    @staticmethod
    def create_provider(req: CreateProviderRequest, use_case: CreateProviderUseCase) -> AIProviderResponse:
        cmd = CreateProviderCommand(**req.dict())
        provider = use_case.execute(cmd)
        return AIProvidersViewMapper.provider(provider)

    @staticmethod
    def update_provider(provider_id: uuid.UUID, req: UpdateProviderRequest, use_case: UpdateProviderUseCase) -> Optional[AIProviderResponse]:
        cmd = UpdateProviderCommand(id=provider_id, **req.dict(exclude_unset=True))
        provider = use_case.execute(cmd)
        if not provider:
            return None
        return AIProvidersViewMapper.provider(provider)

    @staticmethod
    def delete_provider(provider_id: uuid.UUID, use_case: DeleteProviderUseCase) -> bool:
        cmd = DeleteProviderCommand(id=provider_id)
        return use_case.execute(cmd)

    @staticmethod
    def create_model(req: CreateModelRequest, use_case: CreateModelUseCase) -> AIModelResponse:
        cmd = CreateModelCommand(**req.dict())
        model = use_case.execute(cmd)
        return AIProvidersViewMapper.model(model)

    @staticmethod
    def update_model(model_id: uuid.UUID, req: UpdateModelRequest, use_case: UpdateModelUseCase) -> Optional[AIModelResponse]:
        cmd = UpdateModelCommand(id=model_id, **req.dict(exclude_unset=True))
        model = use_case.execute(cmd)
        if not model:
            return None
        return AIProvidersViewMapper.model(model)

    @staticmethod
    def delete_model(model_id: uuid.UUID, use_case: DeleteModelUseCase) -> bool:
        cmd = DeleteModelCommand(id=model_id)
        return use_case.execute(cmd)


