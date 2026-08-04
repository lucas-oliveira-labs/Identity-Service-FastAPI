from fastapi import HTTPException, status

from src.models.user import User
from src.schemas.auth import Login
from src.core.security import verify_password, create_access_token


class AuthService:
    async def login(self, login: Login):
        user = await User.filter(email=login.email).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas"
            )

        if not verify_password(login.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas"
            )

        token = create_access_token({"sub": str(user.id), "email": user.email})

        return {"access_token": token, "token_type": "bearer"}
