from app.modules.auth.application.ports.input.logout_use_case import LogoutUseCase
from app.modules.auth.application.ports.output.refresh_token_repository_port import RefreshTokenRepositoryPort
from app.modules.auth.application.commands.logout.logout_command import LogoutCommand
from app.modules.auth.domain.exceptions.auth_exceptions import InvalidTokenException

class LogoutHandler(LogoutUseCase):
    def __init__(self, refresh_token_repo: RefreshTokenRepositoryPort):
        self.refresh_token_repo = refresh_token_repo

    def execute(self, command: LogoutCommand) -> None:
        token = self.refresh_token_repo.get(command.refresh_token)
        if not token:
            # Idempotent logout - if it doesn't exist, ignore or throw error
            # We'll throw to be explicit, but idempotent is often fine too.
            raise InvalidTokenException("Token not found or already revoked.")
        
        token.revoke()
        self.refresh_token_repo.save(token)
