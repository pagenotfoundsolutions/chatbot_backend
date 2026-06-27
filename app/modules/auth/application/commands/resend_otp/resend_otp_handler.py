import threading
from app.modules.auth.application.ports.output.auth_user_repository_port import AuthUserRepositoryPort
from app.modules.auth.application.commands.resend_otp.resend_otp_command import ResendOtpCommand
from app.shared.services.email import EmailPort

class ResendOtpHandler:
    def __init__(self, user_repo: AuthUserRepositoryPort, email_service: EmailPort):
        self.user_repo = user_repo
        self.email_service = email_service

    def execute(self, command: ResendOtpCommand) -> dict:
        user = self.user_repo.get_by_email(command.email)
        if not user:
            # Silently succeed to prevent email enumeration
            return {"message": "If the email is registered, an OTP has been sent."}
            
        if user.is_verified:
            return {"message": "User is already verified."}
            
        otp = user.generate_otp()
        self.user_repo.save(user)
        
        def send_email():
            self.email_service.send_otp(user.email.value, otp)
            
        threading.Thread(target=send_email, daemon=True).start()
        
        return {"message": "If the email is registered, an OTP has been sent.", "otp_code": otp}
