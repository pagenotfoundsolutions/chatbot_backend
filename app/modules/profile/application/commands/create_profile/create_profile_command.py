from dataclasses import dataclass
from datetime import date
from typing import Optional
from uuid import UUID

@dataclass(frozen=True)
class CreateProfileCommand:
    auth_user_id: UUID
    name: str
    profile_image_url: Optional[str] = None
    dob: Optional[date] = None
