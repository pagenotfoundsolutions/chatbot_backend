from __future__ import annotations
from datetime import datetime
from uuid import UUID, uuid4
from app.shared.kernel.entity import Entity

class RefreshToken(Entity[UUID]):
    def __init__(
        self,
        id: UUID,
        token_string: str,
        user_id: UUID,
        expires_at: datetime,
        is_revoked: bool = False,
        created_at: datetime = None,
        updated_at: datetime = None
    ) -> None:
        super().__init__(id)
        self.token_string = token_string
        self.user_id = user_id
        self.expires_at = expires_at
        self.is_revoked = is_revoked
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or self.created_at

    @classmethod
    def create(cls, token_string: str, user_id: UUID, expires_at: datetime) -> RefreshToken:
        """Factory method to create a new refresh token."""
        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            token_string=token_string,
            user_id=user_id,
            expires_at=expires_at,
            is_revoked=False,
            created_at=now,
            updated_at=now
        )
    
    @property
    def token(self) -> str:
        """The actual token string."""
        return self.token_string
    
    def is_valid(self) -> bool:
        """Check if the token is not revoked and not expired."""
        if self.is_revoked:
            return False
        # Use timezone-naive or aware depending on your app config
        # We assume aware datetimes for robust comparison
        if self.expires_at.tzinfo is None:
            return not self.is_revoked and self.expires_at > datetime.utcnow()
        else:
            from datetime import timezone
            return not self.is_revoked and self.expires_at > datetime.now(timezone.utc)
        
    def revoke(self) -> None:
        """Mark the token as revoked."""
        self.is_revoked = True
        self.updated_at = datetime.utcnow()
