from abc import ABC, abstractmethod
from app.modules.auth.application.commands.logout.logout_command import LogoutCommand

class LogoutUseCase(ABC):
    @abstractmethod
    def execute(self, command: LogoutCommand) -> None:
        pass
