from abc import abstractmethod
from typing import Optional
from uuid import UUID
from app.modules.auth.domain.entities.refresh_token import RefreshToken
from app.shared.kernel.base_repository import BaseRepository

class RefreshTokenRepositoryPort(BaseRepository[RefreshToken, UUID]):
    @abstractmethod
    def get_by_token(self, token_string: str) -> Optional[RefreshToken]:
        pass
