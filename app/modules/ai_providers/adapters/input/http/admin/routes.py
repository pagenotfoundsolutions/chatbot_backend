import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from app.shared.resp import SuccessResp
from app.shared.security.dependencies import get_current_user_id

from app.modules.ai_providers.adapters.input.http.api.schemas import AIProviderResponse, AIModelResponse
from app.modules.ai_providers.adapters.input.http.admin.schemas import CreateProviderRequest, UpdateProviderRequest, CreateModelRequest, UpdateModelRequest
from app.modules.ai_providers.adapters.input.http.admin.controller import AIProvidersAdminController

from app.modules.ai_providers.application.ports.input.create_provider_use_case import CreateProviderUseCase
from app.modules.ai_providers.application.ports.input.update_provider_use_case import UpdateProviderUseCase
from app.modules.ai_providers.application.ports.input.delete_provider_use_case import DeleteProviderUseCase

from app.modules.ai_providers.application.ports.input.create_model_use_case import CreateModelUseCase
from app.modules.ai_providers.application.ports.input.update_model_use_case import UpdateModelUseCase
from app.modules.ai_providers.application.ports.input.delete_model_use_case import DeleteModelUseCase

from app.modules.ai_providers.adapters.input.http.admin.dependencies import (
    get_create_provider_use_case,
    get_update_provider_use_case,
    get_delete_provider_use_case,
    get_create_model_use_case,
    get_update_model_use_case,
    get_delete_model_use_case
)

# TODO: In a production app, we should use a `get_current_admin_user` dependency to enforce RBAC.
# For now, we secure these under /admin and require an authenticated user.
admin_router = APIRouter(tags=["Admin AI Providers"], prefix="/admin/ai-providers")

# --- Provider Routes ---

@admin_router.post("", response_model=SuccessResp[AIProviderResponse], status_code=status.HTTP_201_CREATED)
def create_provider(
    request: CreateProviderRequest,
    use_case: CreateProviderUseCase = Depends(get_create_provider_use_case),
    auth_user_id: UUID = Depends(get_current_user_id),
) -> SuccessResp[AIProviderResponse]:
    provider = AIProvidersAdminController.create_provider(request, use_case)
    return SuccessResp(
        message="Provider created successfully",
        data=provider,
    )

@admin_router.put("/{provider_id}", response_model=SuccessResp[AIProviderResponse])
def update_provider(
    provider_id: uuid.UUID,
    request: UpdateProviderRequest,
    use_case: UpdateProviderUseCase = Depends(get_update_provider_use_case),
    auth_user_id: UUID = Depends(get_current_user_id),
) -> SuccessResp[AIProviderResponse]:
    provider = AIProvidersAdminController.update_provider(provider_id, request, use_case)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return SuccessResp(
        message="Provider updated successfully",
        data=provider,
    )

@admin_router.delete("/{provider_id}", response_model=SuccessResp[None])
def delete_provider(
    provider_id: uuid.UUID,
    use_case: DeleteProviderUseCase = Depends(get_delete_provider_use_case),
    auth_user_id: UUID = Depends(get_current_user_id),
) -> SuccessResp[None]:
    success = AIProvidersAdminController.delete_provider(provider_id, use_case)
    if not success:
        raise HTTPException(status_code=404, detail="Provider not found")
    return SuccessResp(
        message="Provider deleted successfully",
        data=None,
    )

# --- Model Routes ---

@admin_router.post("/models", response_model=SuccessResp[AIModelResponse], status_code=status.HTTP_201_CREATED)
def create_model(
    request: CreateModelRequest,
    use_case: CreateModelUseCase = Depends(get_create_model_use_case),
    auth_user_id: UUID = Depends(get_current_user_id),
) -> SuccessResp[AIModelResponse]:
    model = AIProvidersAdminController.create_model(request, use_case)
    return SuccessResp(
        message="Model created successfully",
        data=model,
    )

@admin_router.put("/models/{model_id}", response_model=SuccessResp[AIModelResponse])
def update_model(
    model_id: uuid.UUID,
    request: UpdateModelRequest,
    use_case: UpdateModelUseCase = Depends(get_update_model_use_case),
    auth_user_id: UUID = Depends(get_current_user_id),
) -> SuccessResp[AIModelResponse]:
    model = AIProvidersAdminController.update_model(model_id, request, use_case)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return SuccessResp(
        message="Model updated successfully",
        data=model,
    )

@admin_router.delete("/models/{model_id}", response_model=SuccessResp[None])
def delete_model(
    model_id: uuid.UUID,
    use_case: DeleteModelUseCase = Depends(get_delete_model_use_case),
    auth_user_id: UUID = Depends(get_current_user_id),
) -> SuccessResp[None]:
    success = AIProvidersAdminController.delete_model(model_id, use_case)
    if not success:
        raise HTTPException(status_code=404, detail="Model not found")
    return SuccessResp(
        message="Model deleted successfully",
        data=None,
    )
