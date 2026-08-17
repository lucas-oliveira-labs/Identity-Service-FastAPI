from fastapi import APIRouter, Depends, status

from src.core.security import get_current_user
from src.models.user import User
from src.schemas.user import UserGet, UserPasswordUpdate, UserUpdate
from src.services.user_service import UserService

router = APIRouter(
    prefix="/users", tags=["Users"], dependencies=[Depends(get_current_user)]
)


@router.get("/", response_model=list[UserGet], status_code=status.HTTP_200_OK)
async def get_user():
    service = UserService()

    return await service.get_all_users()


@router.get("/me", response_model=UserGet, status_code=status.HTTP_200_OK)
async def get_user_me(current_user: User = Depends(get_current_user)):
    service = UserService()
    return await service.get_user_me(current_user)


@router.get("/{user_id}", response_model=UserGet, status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int):
    service = UserService()
    user = await service.get_user_by_id(user_id)
    if not user:
        return {status.HTTP_404_NOT_FOUND: "User not found"}
    else:
        return user


@router.put("/me", response_model=UserGet, status_code=status.HTTP_200_OK)
async def put_user_authenticated(
    user: UserUpdate,
    current_user: User = Depends(get_current_user),
):
    service = UserService()

    return await service.put_user_me(current_user, user)


@router.put("/{user_id}", response_model=UserGet, status_code=status.HTTP_200_OK)
async def put_user_by_id(user_id: int, user: UserUpdate):
    service = UserService()
    return await service.put_user_by_id(user_id, user)


@router.patch("/me/password", status_code=status.HTTP_204_NO_CONTENT)
async def put_user_password(
    password: UserPasswordUpdate, current_user: User = Depends(get_current_user)
):
    service = UserService()

    await service.update_password(current_user, password)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user_by_id(user_id: int):
    service = UserService()
    await service.delete_user_by_id(user_id)

    return {"message": "Usuario deletado com sucesso"}
