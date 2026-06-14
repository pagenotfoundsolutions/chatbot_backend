from dataclasses import dataclass
from datetime import date
from typing import Optional
from uuid import UUID

@dataclass(frozen=True)
class UpdateProfileCommand:
    profile_id: UUID
    name: str
    profile_image_url: Optional[str] = None
    dob: Optional[date] = None
