from fastapi import APIRouter, Depends, status
from typing import Annotated
from uuid import UUID

from app.shared.resp import SuccessResp
from app.modules.profile.adapters.input.http.schemas import (
    CreateProfileRequest,
    UpdateProfileRequest,
    ProfileResponse
)
from app.modules.profile.application.commands.create_profile.create_profile_command import CreateProfileCommand
from app.modules.profile.application.commands.create_profile.create_profile_handler import CreateProfileHandler
from app.modules.profile.application.commands.update_profile.update_profile_command import UpdateProfileCommand
from app.modules.profile.application.commands.update_profile.update_profile_handler import UpdateProfileHandler
from app.modules.profile.application.queries.get_profile.get_profile_query import GetProfileQuery
from app.modules.profile.application.queries.get_profile.get_profile_handler import GetProfileHandler
from app.modules.profile.adapters.input.http.dependencies import (
    get_create_profile_handler,
    get_update_profile_handler,
    get_get_profile_handler
)

router = APIRouter(prefix="/profiles", tags=["Profiles"])

@router.post("", response_model=SuccessResp[ProfileResponse], status_code=status.HTTP_201_CREATED)
def create_profile(
    request: CreateProfileRequest,
    handler: Annotated[CreateProfileHandler, Depends(get_create_profile_handler)]
):
    command = CreateProfileCommand(
        auth_user_id=request.auth_user_id,
        name=request.name,
        profile_image_url=request.profile_image_url,
        dob=request.dob
    )
    profile = handler.execute(command)
    resp_data = ProfileResponse(
        id=profile.id,
        auth_user_id=profile.auth_user_id,
        name=profile.name,
        profile_image_url=profile.profile_image_url,
        dob=profile.dob
    )
    return SuccessResp(message="Profile created successfully", data=resp_data)

@router.put("/{profile_id}", response_model=SuccessResp[ProfileResponse])
def update_profile(
    profile_id: UUID,
    request: UpdateProfileRequest,
    handler: Annotated[UpdateProfileHandler, Depends(get_update_profile_handler)]
):
    command = UpdateProfileCommand(
        profile_id=profile_id,
        name=request.name,
        profile_image_url=request.profile_image_url,
        dob=request.dob
    )
    profile = handler.execute(command)
    resp_data = ProfileResponse(
        id=profile.id,
        auth_user_id=profile.auth_user_id,
        name=profile.name,
        profile_image_url=profile.profile_image_url,
        dob=profile.dob
    )
    return SuccessResp(message="Profile updated successfully", data=resp_data)

@router.get("/user/{auth_user_id}", response_model=SuccessResp[ProfileResponse])
def get_profile_by_user_id(
    auth_user_id: UUID,
    handler: Annotated[GetProfileHandler, Depends(get_get_profile_handler)]
):
    query = GetProfileQuery(auth_user_id=auth_user_id)
    profile = handler.execute(query)
    resp_data = ProfileResponse(
        id=profile.id,
        auth_user_id=profile.auth_user_id,
        name=profile.name,
        profile_image_url=profile.profile_image_url,
        dob=profile.dob
    )
    return SuccessResp(message="Profile retrieved successfully", data=resp_data)
