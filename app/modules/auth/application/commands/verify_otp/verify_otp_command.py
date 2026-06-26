from pydantic import BaseModel, EmailStr

class VerifyOtpCommand(BaseModel):
    email: EmailStr
    otp_code: str
