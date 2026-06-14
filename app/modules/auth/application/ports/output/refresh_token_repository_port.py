from typing import Optional
from app.modules.auth.domain.entities.refresh_token import RefreshToken
from app.shared.kernel.base_repository import BaseRepository

class RefreshTokenRepositoryPort(BaseRepository[RefreshToken, str]):
    # BaseRepository already requires save(), get(), and delete()
    pass
