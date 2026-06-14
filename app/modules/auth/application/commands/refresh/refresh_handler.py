from datetime import datetime, timedelta
from app.modules.auth.application.ports.input.refresh_use_case import RefreshUseCase
from app.modules.auth.application.ports.output.token_generator_port import TokenGeneratorPort
from app.modules.auth.application.ports.output.refresh_token_repository_port import RefreshTokenRepositoryPort
from app.modules.auth.application.commands.refresh.refresh_command import RefreshCommand
from app.modules.auth.domain.exceptions.auth_exceptions import InvalidTokenException
from app.modules.auth.application.dto.token_result import TokenResult
from app.modules.auth.domain.entities.refresh_token import RefreshToken
from app.modules.auth.infrastructure.config.auth_config import get_auth_config

class RefreshHandler(RefreshUseCase):
    def __init__(
        self,
        token_generator: TokenGeneratorPort,
        refresh_token_repo: RefreshTokenRepositoryPort
    ):
        self.token_generator = token_generator
        self.refresh_token_repo = refresh_token_repo
        self.config = get_auth_config()

    def execute(self, command: RefreshCommand) -> TokenResult:
        # Retrieve the old refresh token
        old_token = self.refresh_token_repo.get(command.refresh_token)
        if not old_token or not old_token.is_valid():
            raise InvalidTokenException("Invalid or expired refresh token.")

        # Revoke the old token (Token rotation)
        old_token.revoke()
        self.refresh_token_repo.save(old_token)

        # Issue new tokens
        access_token = self.token_generator.generate_access_token(old_token.user_id)
        new_refresh_token_str = self.token_generator.generate_refresh_token(old_token.user_id)

        expires_at = datetime.utcnow() + timedelta(days=self.config.refresh_token_expire_days)
        new_refresh_token = RefreshToken.create(
            token_string=new_refresh_token_str,
            user_id=old_token.user_id,
            expires_at=expires_at
        )
        self.refresh_token_repo.save(new_refresh_token)

        return TokenResult(
            access_token=access_token,
            refresh_token=new_refresh_token_str,
            user_id=old_token.user_id
        )
