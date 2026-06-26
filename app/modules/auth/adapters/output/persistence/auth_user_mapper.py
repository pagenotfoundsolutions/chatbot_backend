from uuid import UUID
from app.modules.auth.domain.entities.auth_user import AuthUser
from app.modules.auth.domain.value_objects.email import Email
from app.modules.auth.adapters.output.persistence.models.auth_user_model import AuthUserModel

class AuthUserMapper:
    """Maps between the Domain User Aggregate and the SQLAlchemy AuthUserModel."""
    
    @staticmethod
    def to_domain(model: AuthUserModel) -> AuthUser:
        """Converts SQLAlchemy AuthUserModel to Domain User Entity."""
        user = AuthUser(
            id=model.id,
            email=Email(model.email),
            hashed_password=model.hashed_password
        )
        user.is_verified = model.is_verified
        user.otp_code = model.otp_code
        user.otp_expires_at = model.otp_expires_at
        return user
    
    @staticmethod
    def to_persistence(entity: AuthUser) -> AuthUserModel:
        """Converts Domain User Entity to SQLAlchemy AuthUserModel."""
        return AuthUserModel(
            id=entity.id,
            email=entity.email.value,
            hashed_password=entity.hashed_password,
            is_verified=entity.is_verified,
            otp_code=entity.otp_code,
            otp_expires_at=entity.otp_expires_at
        )
