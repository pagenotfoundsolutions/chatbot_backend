import smtplib
from email.message import EmailMessage
from typing import Protocol

from app.shared.config.settings import settings

class EmailPort(Protocol):
    def send_otp(self, to_email: str, otp_code: str) -> None:
        """Send an OTP code to the given email address."""
        ...

class SmtpEmailAdapter(EmailPort):
    def send_otp(self, to_email: str, otp_code: str) -> None:
        msg = EmailMessage()
        msg.set_content(f"Hello,\n\nYour OTP code for verification is: {otp_code}\nThis code will expire in 10 minutes.\n\nThank you!")
        msg["Subject"] = "Your Verification OTP"
        msg["From"] = settings.smtp_user
        msg["To"] = to_email

        try:
            if settings.smtp_use_tls:
                with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
                    server.starttls()
                    server.login(settings.smtp_user, settings.smtp_password)
                    server.send_message(msg)
            else:
                with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
                    server.login(settings.smtp_user, settings.smtp_password)
                    server.send_message(msg)
        except Exception as e:
            # For production, we should log this error properly.
            print(f"Failed to send email to {to_email}: {e}")
