from abc import abstractmethod
from typing import Optional
from uuid import UUID

from app.modules.profile.domain.entities.profile import Profile
from app.shared.kernel.base_repository import BaseRepository

class ProfileRepositoryPort(BaseRepository[Profile, UUID]):
    @abstractmethod
    def get_by_auth_user_id(self, auth_user_id: UUID) -> Optional[Profile]:
        pass
