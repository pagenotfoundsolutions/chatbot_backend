from app.modules.ai_providers.application.ports.input.list_providers_with_active_models_usecase import ListProvidersWithActiveModelsUseCase
import uuid
from typing import List, Optional

from app.modules.ai_providers.adapters.input.http.api.schemas import AIProviderResponse, AIModelResponse
from app.modules.ai_providers.adapters.input.http.mappers.view_mapper import AIProvidersViewMapper

from app.modules.ai_providers.application.ports.input.list_providers_use_case import ListProvidersUseCase
from app.modules.ai_providers.application.ports.input.get_provider_use_case import GetProviderUseCase
from app.modules.ai_providers.application.ports.input.list_models_use_case import ListModelsUseCase
from app.modules.ai_providers.application.ports.input.list_active_models_use_case import ListActiveModelsUseCase
from app.modules.ai_providers.application.ports.input.get_model_use_case import GetModelUseCase

class AIProvidersApiController:
    @staticmethod
    def list_providers(use_case: ListProvidersUseCase) -> List[AIProviderResponse]:
        providers = use_case.execute()
        return [AIProvidersViewMapper.provider(p) for p in providers]

    @staticmethod
    def get_provider(provider_id: uuid.UUID, use_case: GetProviderUseCase) -> Optional[AIProviderResponse]:
        provider = use_case.execute(provider_id)
        if not provider:
            return None
        return AIProvidersViewMapper.provider(provider)

    @staticmethod
    def list_models(use_case: ListModelsUseCase) -> List[AIModelResponse]:
        models = use_case.execute()
        return [AIProvidersViewMapper.model(m) for m in models]

    @staticmethod
    def list_active_models(use_case: ListActiveModelsUseCase) -> List[AIModelResponse]:
        models = use_case.execute()
        return [AIProvidersViewMapper.model(m) for m in models]

    @staticmethod
    def get_model(model_id: uuid.UUID, use_case: GetModelUseCase) -> Optional[AIModelResponse]:
        model = use_case.execute(model_id)
        if not model:
            return None
        return AIProvidersViewMapper.model(model)
    
    @staticmethod
    def list_providers_with_active_models(use_case: ListProvidersWithActiveModelsUseCase) -> List[AIProviderResponse]:
        providers = use_case.execute()
        return [AIProvidersViewMapper.provider(p) for p in providers]
