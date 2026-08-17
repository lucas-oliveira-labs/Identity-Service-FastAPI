from fastapi import APIRouter, Depends

from src.core.security import get_current_user
from src.schemas.auth import Login, RefreshToken
from src.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login(login: Login, service: AuthService = Depends()):
    return await service.login(login)


@router.post("/refresh")
async def refresh(data: RefreshToken, service: AuthService = Depends()):
    return await service.refresh_token(data.refresh_token)


@router.post("/logout")
async def logout(
    current_user=Depends(get_current_user), service: AuthService = Depends()
):
    return await service.logout(current_user)
