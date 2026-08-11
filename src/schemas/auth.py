from pydantic import BaseModel, EmailStr, Field


class Login(BaseModel):
    email: str
    password: str


class RefreshToken(BaseModel):
    refresh_token: str


class ForgotPassword(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)
