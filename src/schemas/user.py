from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserCreate(BaseModel):
    full_name: str = Field(None, min_length=2, max_length=100)
    email: EmailStr = Field(..., min_length=8, max_length=255)
    password: str = Field(..., min_length=6, max_length=255)


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = Field(None, min_length=8, max_length=255)
    password: Optional[str] = Field(None, min_length=6, max_length=255)


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
