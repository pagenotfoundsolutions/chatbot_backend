from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class TokenResult:
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    user_id: UUID | None = None
