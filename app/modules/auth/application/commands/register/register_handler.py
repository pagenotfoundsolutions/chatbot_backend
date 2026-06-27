
import threading
from app.modules.auth.application.ports.input.register_use_case import RegisterUseCase
from app.modules.auth.application.ports.output.auth_user_repository_port import AuthUserRepositoryPort
from app.modules.auth.application.ports.output.password_hasher_port import PasswordHasherPort
from app.modules.auth.application.commands.register.register_command import RegisterCommand
from app.modules.auth.domain.entities.auth_user import AuthUser
from app.modules.auth.domain.exceptions.auth_exceptions import AuthUserAlreadyExistsException
from app.modules.auth.application.dto.register_result import RegisterResult
from app.shared.services.email import EmailPort

class RegisterHandler(RegisterUseCase):

    def __init__(
        self, 
        user_repo: AuthUserRepositoryPort, 
        password_hasher: PasswordHasherPort,
        email_service: EmailPort
    ):
        self.user_repo = user_repo
        self.password_hasher = password_hasher
        self.email_service = email_service

    def execute(self, command: RegisterCommand) -> RegisterResult:
        if self.user_repo.get_by_email(command.email):
            raise AuthUserAlreadyExistsException(command.email)
            
        hashed_password = self.password_hasher.hash(command.password)
        user = AuthUser.create(command.email, hashed_password)
        
        otp = user.generate_otp()
        self.user_repo.save(user)
        
        def send_email():
            self.email_service.send_otp(user.email.value, otp)
            
        threading.Thread(target=send_email, daemon=True).start()
        
        return RegisterResult(id=user.id, email=user.email.value, otp_code=otp)