from abc import ABC, abstractmethod
from app.modules.auth.application.commands.login.login_command import LoginCommand
from app.modules.auth.application.dto.token_result import TokenResult

class LoginUseCase(ABC):
    @abstractmethod
    def execute(self, command: LoginCommand) -> TokenResult:
        pass
