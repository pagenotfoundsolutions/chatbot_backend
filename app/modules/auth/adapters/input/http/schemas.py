from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str = Field(..., description="The refresh token to use for generating a new access token.")

class LogoutRequest(BaseModel):
    refresh_token: str = Field(..., description="The refresh token to invalidate.")

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"

class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp_code: str = Field(..., description="The 6-digit OTP code")

class ResendOtpRequest(BaseModel):
    email: EmailStr
