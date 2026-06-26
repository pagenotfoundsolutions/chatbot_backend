from app.modules.auth.application.ports.output.auth_user_repository_port import AuthUserRepositoryPort
from app.modules.auth.application.commands.verify_otp.verify_otp_command import VerifyOtpCommand
from app.modules.auth.domain.exceptions.auth_exceptions import InvalidCredentialsException

class VerifyOtpHandler:
    def __init__(self, user_repo: AuthUserRepositoryPort):
        self.user_repo = user_repo

    def execute(self, command: VerifyOtpCommand) -> dict:
        user = self.user_repo.get_by_email(command.email)
        if not user:
            raise InvalidCredentialsException()
            
        user.verify_otp(command.otp_code)
        self.user_repo.save(user)
        return {"message": "Email verified successfully."}
