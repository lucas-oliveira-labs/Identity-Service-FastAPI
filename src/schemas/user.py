from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    email: EmailStr = Field(..., min_length=8, max_length=255)
    password: str = Field(..., min_length=6, max_length=255)


class UserGet(BaseModel):
    id: int
    nome: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = Field(None, min_length=8, max_length=255)
    password: Optional[str] = Field(None, min_length=6, max_length=255)


class UserResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        from_attributes = True
