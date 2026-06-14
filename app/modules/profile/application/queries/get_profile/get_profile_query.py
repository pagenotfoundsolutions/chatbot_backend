from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class GetProfileQuery:
    auth_user_id: UUID
