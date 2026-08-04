from fastapi import APIRouter, status, Depends
from src.schemas.user import UserGet, UserUpdate
from src.services.user_service import UserService
from src.core.security import get_current_user


router = APIRouter(
    prefix="/users", tags=["Users"], dependencies=[Depends(get_current_user)]
)


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


@router.put("/{user_id}", response_model=UserGet, status_code=status.HTTP_200_OK)
async def put_user_by_id(user_id: int, user: UserUpdate):
    service = UserService()
    return await service.put_user_by_id(user_id, user)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user_by_id(user_id: int):
    service = UserService()
    await service.delete_user_by_id(user_id)

    return {"message": "Usuario deletado com sucesso"}
