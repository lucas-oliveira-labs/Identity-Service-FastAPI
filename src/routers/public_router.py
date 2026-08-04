from fastapi import APIRouter, Depends, status
from src.schemas.user import UserCreate
from src.services.user_service import UserService


router = APIRouter(prefix="/created", tags=["created"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, service: UserService = Depends()):
    return await service.create_user(user)
