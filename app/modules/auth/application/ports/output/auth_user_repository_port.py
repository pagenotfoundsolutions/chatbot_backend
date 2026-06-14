from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from app.modules.auth.domain.entities.auth_user import AuthUser
from app.shared.kernel.base_repository import BaseRepository

class AuthUserRepositoryPort(BaseRepository[AuthUser, UUID]):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[AuthUser]:
        pass