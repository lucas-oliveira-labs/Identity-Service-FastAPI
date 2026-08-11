from fastapi import APIRouter, Depends, status
from src.schemas.user import UserCreate
from src.schemas.auth import ForgotPassword
from src.services.user_service import UserService
from src.services.AuthService import AuthService


router = APIRouter(prefix="/created", tags=["created"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, service: UserService = Depends()):
    return await service.create_user(user)


@router.post("/forgot-password", status_code=status.HTTP_202_ACCEPTED)
async def forgot_password(data: ForgotPassword):
    service = AuthService()

    return await service.forgot_password(data)
