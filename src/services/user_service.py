from src.models.user import User
from src.schemas.user import UserCreate


class UserService:
    async def create_user(self, user: UserCreate):
        existing_user = await User.filter(email=user.email).first()

        if existing_user:
            raise Exception("Email já cadastrado")

        new_user = await User.create(
            nome=user.nome, email=user.email, password_hash=user.password
        )
        return new_user
