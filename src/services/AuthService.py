from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status

from src.models.user import User
from src.models.refresh_token import RefreshToken
from src.schemas.auth import Login
from src.core.security import verify_password
from src.services.jwt_service import create_access_token, create_refresh_token


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

        payload = {
            "sub": str(user.id),
            "email": user.email,
        }

        access_token = create_access_token(payload)

        refresh_token = create_refresh_token(payload)

        expires_at = datetime.now(timezone.utc) + timedelta(days=7)

        await RefreshToken.create(token=refresh_token, user=user, expires_at=expires_at)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
