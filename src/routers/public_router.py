from fastapi import APIRouter, Depends, status
from src.schemas.user import UserCreate, UserGet
from src.services.user_service import UserService


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, service: UserService = Depends()):
    return await service.create_user(user)


@router.get("/", response_model=list[UserGet], status_code=status.HTTP_200_OK)
async def get_user():
    service = UserService()

    return await service.get_all_users()


@router.get("/{user_id}", response_model=UserGet, status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int):
    service = UserService()
    user = await service.get_user_by_id(user_id)
    if not user:
        return {status.HTTP_404_NOT_FOUND: "User not found"}
    else:
        return user
