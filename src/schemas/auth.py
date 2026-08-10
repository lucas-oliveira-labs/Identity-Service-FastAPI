from pydantic import BaseModel, EmailStr


class Login(BaseModel):
    email: str
    password: str


class RefreshToken(BaseModel):
    refresh_token: str


class ForgotPassword(BaseModel):
    email: EmailStr
