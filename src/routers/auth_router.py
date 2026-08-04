from fastapi import APIRouter, Depends
from src.services.AuthService import AuthService
from src.schemas.auth import Login


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login(login: Login, service: AuthService = Depends()):
    return await service.login(login)
