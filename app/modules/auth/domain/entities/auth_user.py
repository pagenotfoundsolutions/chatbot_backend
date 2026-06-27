from __future__ import annotations
from uuid import UUID, uuid4
from datetime import datetime, timezone, timedelta
import random

from app.modules.auth.domain.value_objects.email import Email
from app.shared.kernel.aggregate_root import AggregateRoot
from app.modules.auth.domain.exceptions.auth_exceptions import InvalidOtpException

class AuthUser(AggregateRoot[UUID]):
    def __init__(
        self, 
        id: UUID, 
        email: Email, 
        hashed_password: str,
        is_verified: bool = False,
        otp_code: str | None = None,
        otp_expires_at: datetime | None = None
    ) -> None:
        super().__init__(id)
        self.email = email
        self.hashed_password = hashed_password
        self.is_verified = is_verified
        self.otp_code = otp_code
        self.otp_expires_at = otp_expires_at

    @classmethod
    def create(cls, email: str, hashed_password: str) -> AuthUser:
        """Factory method to create a new user."""
        return cls(
            id=uuid4(),
            email=Email(email),
            hashed_password=hashed_password,
            is_verified=False
        )

    def generate_otp(self) -> str:
        """Generate a 4-digit OTP and set its expiry to 10 minutes from now."""
        self.otp_code = str(random.randint(1000, 9999))
        self.otp_expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
        return self.otp_code

    def verify_otp(self, otp_code: str) -> None:
        """Verifies the given OTP code."""
        if self.is_verified:
            return
            
        if not self.otp_code or not self.otp_expires_at:
            raise InvalidOtpException("No OTP has been generated for this user.")
            
        # Ensure we compare timezone-aware datetimes. Convert now to UTC.
        now_utc = datetime.now(timezone.utc)
        if now_utc > self.otp_expires_at:
            raise InvalidOtpException("OTP has expired. Please request a new one.")
            
        if self.otp_code != otp_code:
            raise InvalidOtpException("Invalid OTP code.")
            
        self.is_verified = True
        self.otp_code = None
        self.otp_expires_at = None

