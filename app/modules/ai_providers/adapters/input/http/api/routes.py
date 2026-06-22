from app.modules.ai_providers.adapters.input.http.api.dependencies import get_list_providers_with_active_models_use_case
from app.modules.ai_providers.application.ports.input.list_providers_with_active_models_usecase import ListProvidersWithActiveModelsUseCase
import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from app.shared.resp import SuccessResp
from app.shared.security.dependencies import get_current_user_id

from app.modules.ai_providers.adapters.input.http.api.schemas import AIProviderResponse, AIModelResponse
from app.modules.ai_providers.adapters.input.http.api.controller import AIProvidersApiController
from app.modules.ai_providers.application.ports.input.list_providers_use_case import ListProvidersUseCase
from app.modules.ai_providers.application.ports.input.get_provider_use_case import GetProviderUseCase
from app.modules.ai_providers.application.ports.input.list_models_use_case import ListModelsUseCase
from app.modules.ai_providers.application.ports.input.list_active_models_use_case import ListActiveModelsUseCase
from app.modules.ai_providers.application.ports.input.get_model_use_case import GetModelUseCase

from app.modules.ai_providers.adapters.input.http.api.dependencies import (
    get_list_providers_use_case,
    get_get_provider_use_case,
    get_list_models_use_case,
    get_list_active_models_use_case,
    get_get_model_use_case
)

router = APIRouter(prefix="/ai", tags=["AI Providers and Models"])

@router.get("/providers", response_model=SuccessResp[List[AIProviderResponse]])
def list_providers(
    use_case: ListProvidersUseCase = Depends(get_list_providers_use_case),
    auth_user_id: UUID = Depends(get_current_user_id),
) -> SuccessResp[List[AIProviderResponse]]:
    return SuccessResp(
        message="Providers fetched",
        data=AIProvidersApiController.list_providers(use_case),
    )

@router.get("/providers/with-active-models", response_model=SuccessResp[List[AIProviderResponse]])
def list_providers_with_active_models(
    use_case: ListProvidersWithActiveModelsUseCase = Depends(get_list_providers_with_active_models_use_case),
) -> SuccessResp[List[AIProviderResponse]]:
    return SuccessResp(
        message="Providers with active models fetched",
        data=AIProvidersApiController.list_providers_with_active_models(use_case),
    )

@router.get("/providers/{provider_id}", response_model=SuccessResp[AIProviderResponse])
def get_provider(
    provider_id: uuid.UUID,
    use_case: GetProviderUseCase = Depends(get_get_provider_use_case),
) -> SuccessResp[AIProviderResponse]:
    provider = AIProvidersApiController.get_provider(provider_id, use_case)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return SuccessResp(
        message="Provider fetched",
        data=provider,
    )

@router.get("/models", response_model=SuccessResp[List[AIModelResponse]])
def list_models(
    use_case: ListModelsUseCase = Depends(get_list_models_use_case),
) -> SuccessResp[List[AIModelResponse]]:
    return SuccessResp(
        message="Models fetched",
        data=AIProvidersApiController.list_models(use_case),
    )

@router.get("/models/active", response_model=SuccessResp[List[AIModelResponse]])
def list_active_models(
    use_case: ListActiveModelsUseCase = Depends(get_list_active_models_use_case),
) -> SuccessResp[List[AIModelResponse]]:
    return SuccessResp(
        message="Active models fetched",
        data=AIProvidersApiController.list_active_models(use_case),
    )

@router.get("/models/{model_id}", response_model=SuccessResp[AIModelResponse])
def get_model(
    model_id: uuid.UUID,
    use_case: GetModelUseCase = Depends(get_get_model_use_case),
) -> SuccessResp[AIModelResponse]:
    model = AIProvidersApiController.get_model(model_id, use_case)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return SuccessResp(
        message="Model fetched",
        data=model,
    )
