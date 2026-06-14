from pydantic import BaseModel, EmailStr, Field

class RegisterCommand(BaseModel):
    email: EmailStr
    # You can add length validation for the password right here!
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")

    class Config:
        frozen = True
