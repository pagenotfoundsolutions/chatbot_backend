from abc import ABC, abstractmethod
from app.modules.auth.application.commands.refresh.refresh_command import RefreshCommand
from app.modules.auth.application.dto.token_result import TokenResult

class RefreshUseCase(ABC):
    @abstractmethod
    def execute(self, command: RefreshCommand) -> TokenResult:
        pass
