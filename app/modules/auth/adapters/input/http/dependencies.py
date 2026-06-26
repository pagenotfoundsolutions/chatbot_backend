from fastapi import Depends
from sqlalchemy.orm import Session
from app.shared.database.session import get_db

from app.modules.auth.application.ports.input.register_use_case import RegisterUseCase
from app.modules.auth.application.commands.register.register_handler import RegisterHandler
from app.modules.auth.adapters.output.persistence.sqlalchemy_auth_user_repository import SqlAlchemyAuthUserRepository
from app.modules.auth.adapters.output.security.bcrypt_password_hasher import BcryptPasswordHasher

from app.modules.auth.application.ports.input.login_use_case import LoginUseCase
from app.modules.auth.application.commands.login.login_handler import LoginHandler
from app.modules.auth.application.ports.input.logout_use_case import LogoutUseCase
from app.modules.auth.application.commands.logout.logout_handler import LogoutHandler
from app.modules.auth.application.ports.input.refresh_use_case import RefreshUseCase
from app.modules.auth.application.commands.refresh.refresh_handler import RefreshHandler

from app.modules.auth.adapters.output.persistence.sqlalchemy_refresh_token_repository import SqlAlchemyRefreshTokenRepository
from app.modules.auth.adapters.output.security.jwt_token_generator import PyJwtTokenGenerator

from app.shared.services.email import SmtpEmailAdapter
from app.modules.auth.application.commands.verify_otp.verify_otp_handler import VerifyOtpHandler
from app.modules.auth.application.commands.resend_otp.resend_otp_handler import ResendOtpHandler

# State-less providers as Singletons
password_hasher = BcryptPasswordHasher()
token_generator = PyJwtTokenGenerator()
email_adapter = SmtpEmailAdapter()

def get_register_use_case(
    db_session: Session = Depends(get_db)
) -> RegisterUseCase:
    user_repository = SqlAlchemyAuthUserRepository(session=db_session)
    return RegisterHandler(
        user_repo=user_repository,
        password_hasher=password_hasher,
        email_service=email_adapter
    )

def get_login_use_case(
    db_session: Session = Depends(get_db)
) -> LoginUseCase:
    user_repository = SqlAlchemyAuthUserRepository(session=db_session)
    refresh_repo = SqlAlchemyRefreshTokenRepository(session=db_session)
    return LoginHandler(
        user_repo=user_repository,
        password_hasher=password_hasher,
        token_generator=token_generator,
        refresh_token_repo=refresh_repo,
        email_service=email_adapter
    )

def get_logout_use_case(
    db_session: Session = Depends(get_db)
) -> LogoutUseCase:
    refresh_repo = SqlAlchemyRefreshTokenRepository(session=db_session)
    return LogoutHandler(refresh_token_repo=refresh_repo)

def get_refresh_use_case(
    db_session: Session = Depends(get_db)
) -> RefreshUseCase:
    refresh_repo = SqlAlchemyRefreshTokenRepository(session=db_session)
    return RefreshHandler(
        token_generator=token_generator,
        refresh_token_repo=refresh_repo
    )

def get_verify_otp_use_case(
    db_session: Session = Depends(get_db)
) -> VerifyOtpHandler:
    user_repository = SqlAlchemyAuthUserRepository(session=db_session)
    return VerifyOtpHandler(user_repo=user_repository)

def get_resend_otp_use_case(
    db_session: Session = Depends(get_db)
) -> ResendOtpHandler:
    user_repository = SqlAlchemyAuthUserRepository(session=db_session)
    return ResendOtpHandler(
        user_repo=user_repository,
        email_service=email_adapter
    )
