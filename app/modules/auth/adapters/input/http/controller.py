from fastapi import APIRouter, Depends
from .schemas import RegisterRequest, LoginRequest, RefreshRequest, LogoutRequest, TokenResponse
from app.modules.auth.application.dto.register_result import RegisterResult
from app.modules.auth.application.ports.input.register_use_case import RegisterUseCase
from app.modules.auth.application.commands.register.register_command import RegisterCommand

from app.modules.auth.application.ports.input.login_use_case import LoginUseCase
from app.modules.auth.application.commands.login.login_command import LoginCommand

from app.modules.auth.application.ports.input.refresh_use_case import RefreshUseCase
from app.modules.auth.application.commands.refresh.refresh_command import RefreshCommand

from app.modules.auth.application.ports.input.logout_use_case import LogoutUseCase
from app.modules.auth.application.commands.logout.logout_command import LogoutCommand

from app.shared.resp import SuccessResp

from .dependencies import (
    get_register_use_case,
    get_login_use_case,
    get_refresh_use_case,
    get_logout_use_case
)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=SuccessResp[RegisterResult])
def register(request: RegisterRequest, use_case: RegisterUseCase = Depends(get_register_use_case)):
    command = RegisterCommand(
        email=request.email,
        password=request.password
    )
    result = use_case.execute(command)
    return SuccessResp(
        message="AuthUser registered successfully",
        data=result
    )

@router.post("/login", response_model=SuccessResp[TokenResponse])
def login(request: LoginRequest, use_case: LoginUseCase = Depends(get_login_use_case)):
    command = LoginCommand(
        email=request.email,
        password=request.password
    )
    result = use_case.execute(command)
    return SuccessResp(
        message="Login successful",
        data=result
    )

@router.post("/refresh", response_model=SuccessResp[TokenResponse])
def refresh_token(request: RefreshRequest, use_case: RefreshUseCase = Depends(get_refresh_use_case)):
    command = RefreshCommand(refresh_token=request.refresh_token)
    result = use_case.execute(command)
    return SuccessResp(
        message="Token refreshed successfully",
        data=result
    )

@router.post("/logout", response_model=SuccessResp[None])
def logout(request: LogoutRequest, use_case: LogoutUseCase = Depends(get_logout_use_case)):
    command = LogoutCommand(refresh_token=request.refresh_token)
    use_case.execute(command)
    return SuccessResp(
        message="Logged out successfully",
        data=None
    )

