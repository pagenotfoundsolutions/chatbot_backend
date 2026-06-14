from datetime import datetime, timedelta
from app.modules.auth.application.ports.input.login_use_case import LoginUseCase
from app.modules.auth.application.ports.output.auth_user_repository_port import AuthUserRepositoryPort
from app.modules.auth.application.ports.output.password_hasher_port import PasswordHasherPort
from app.modules.auth.application.ports.output.token_generator_port import TokenGeneratorPort
from app.modules.auth.application.ports.output.refresh_token_repository_port import RefreshTokenRepositoryPort
from app.modules.auth.application.commands.login.login_command import LoginCommand
from app.modules.auth.domain.exceptions.auth_exceptions import InvalidCredentialsException
from app.modules.auth.application.dto.token_result import TokenResult
from app.modules.auth.domain.entities.refresh_token import RefreshToken
from app.modules.auth.infrastructure.config.auth_config import get_auth_config

class LoginHandler(LoginUseCase):
    def __init__(
        self,
        user_repo: AuthUserRepositoryPort,
        password_hasher: PasswordHasherPort,
        token_generator: TokenGeneratorPort,
        refresh_token_repo: RefreshTokenRepositoryPort
    ):
        self.user_repo = user_repo
        self.password_hasher = password_hasher
        self.token_generator = token_generator
        self.refresh_token_repo = refresh_token_repo
        self.config = get_auth_config()

    def execute(self, command: LoginCommand) -> TokenResult:
        user = self.user_repo.get_by_email(command.email)
        if not user:
            raise InvalidCredentialsException()

        if not self.password_hasher.verify(command.password, user.hashed_password):
            raise InvalidCredentialsException()

        access_token = self.token_generator.generate_access_token(user.id)
        refresh_token_str = self.token_generator.generate_refresh_token(user.id)

        expires_at = datetime.utcnow() + timedelta(days=self.config.refresh_token_expire_days)
        refresh_token = RefreshToken.create(
            token_string=refresh_token_str,
            user_id=user.id,
            expires_at=expires_at
        )
        self.refresh_token_repo.save(refresh_token)

        return TokenResult(
            access_token=access_token,
            refresh_token=refresh_token_str,
            user_id=user.id
        )
