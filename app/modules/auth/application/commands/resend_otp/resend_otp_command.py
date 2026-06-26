from pydantic import BaseModel, EmailStr

class ResendOtpCommand(BaseModel):
    email: EmailStr
