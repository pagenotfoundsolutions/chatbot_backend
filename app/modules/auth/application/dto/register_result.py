from pydantic import BaseModel
from uuid import UUID

class RegisterResult(BaseModel):
    id: UUID
    email: str
