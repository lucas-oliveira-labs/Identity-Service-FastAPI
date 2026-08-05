from pydantic import BaseModel


class Login(BaseModel):
    email: str
    password: str


class RefreshToken(BaseModel):
    refresh_token: str
