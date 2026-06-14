from __future__ import annotations
from uuid import UUID, uuid4
from app.modules.auth.domain.value_objects.email import Email
from app.shared.kernel.aggregate_root import AggregateRoot

class AuthUser(AggregateRoot[UUID]):
    def __init__(self, id: UUID, email: Email, hashed_password: str) -> None:
        super().__init__(id)
        self.email = email
        self.hashed_password = hashed_password

    @classmethod
    def create(cls, email: str, hashed_password: str) -> AuthUser:
        """Factory method to create a new user."""
        return cls(
            id=uuid4(),
            email=Email(email),
            hashed_password=hashed_password
        )
