from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from uuid import UUID

class CreateProfileRequest(BaseModel):
    name: str = Field(..., min_length=2)
    profile_image_url: Optional[str] = None
    dob: Optional[date] = None

class UpdateProfileRequest(BaseModel):
    name: str = Field(..., min_length=2)
    profile_image_url: Optional[str] = None
    dob: Optional[date] = None

class ProfileResponse(BaseModel):
    id: UUID
    name: str
    profile_image_url: Optional[str]
    dob: Optional[date]
