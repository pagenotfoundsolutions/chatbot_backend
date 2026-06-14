from uuid import UUID
from app.modules.auth.domain.entities.auth_user import AuthUser
from app.modules.auth.domain.value_objects.email import Email
from app.modules.auth.adapters.output.persistence.models.auth_user_model import AuthUserModel

class AuthUserMapper:
    """Maps between the Domain User Aggregate and the SQLAlchemy AuthUserModel."""
    
    @staticmethod
    def to_domain(model: AuthUserModel) -> AuthUser:
        """Converts SQLAlchemy AuthUserModel to Domain User Entity."""
        return AuthUser(
            id=UUID(model.id),
            email=Email(model.email),
            hashed_password=model.hashed_password
        )
    
    @staticmethod
    def to_persistence(entity: AuthUser) -> AuthUserModel:
        """Converts Domain User Entity to SQLAlchemy AuthUserModel."""
        return AuthUserModel(
            id=str(entity.id),
            email=entity.email.value,
            hashed_password=entity.hashed_password
        )
