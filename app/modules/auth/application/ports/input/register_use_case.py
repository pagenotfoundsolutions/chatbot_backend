from abc import ABC, abstractmethod
from app.modules.auth.application.commands.register.register_command import RegisterCommand
from app.modules.auth.application.dto.register_result import RegisterResult


class RegisterUseCase(ABC):
    @abstractmethod
    def execute(self, command: RegisterCommand) -> RegisterResult:
        pass