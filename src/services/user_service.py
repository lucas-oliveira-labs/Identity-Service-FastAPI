from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate
from fastapi import HTTPException, status
from src.core.security import hash_password


class UserService:
    async def create_user(self, user: UserCreate):
        existing_user = await User.filter(email=user.email).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email já cadastrado"
            )

        new_user = await User.create(
            nome=user.nome, email=user.email, password_hash=hash_password(user.password)
        )
        return new_user

    async def get_all_users(self):
        return await User.all()

    async def get_user_by_id(self, user_id: int):
        return await User.filter(id=user_id).first()

    async def get_user_me(self, current_user: User):
        return current_user

    async def put_user_by_id(self, user_id: int, user: UserUpdate):
        existing_user = await User.filter(id=user_id).first()

        if existing_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
            )

        existing_user.nome = user.nome
        existing_user.email = user.email

        await existing_user.save()
        return existing_user

    async def put_user_me(self, current_user: User, user: UserUpdate):
        if user.email is not None:
            email_exists = (
                await User.filter(email=user.email).exclude(id=current_user.id).exists()
            )

            if email_exists:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Email já cadastrado"
                )
            current_user.email = user.email

        if user.nome is not None:
            current_user.nome = user.nome

        await current_user.save()

        return current_user

    async def delete_user_by_id(self, user_id: int):
        user = await User.get_or_none(id=user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
            )

        await user.delete()
