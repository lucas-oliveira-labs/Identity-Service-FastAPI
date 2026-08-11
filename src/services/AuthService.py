from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from fastapi import HTTPException, status
import os

from src.models.user import User
from src.models.refresh_token import RefreshToken
from src.models.password_reset_token import PasswordResetToken
from src.schemas.auth import Login, ForgotPassword, ResetPassword
from src.core.security import (
    verify_password,
    generate_password_reset_token,
    hash_password_reset_token,
    hash_password,
)
from src.services.jwt_service import create_access_token, create_refresh_token
from src.services.email_service import EmailService


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


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

        access_token = create_access_token({"sub": str(user.id)})

        refresh_token = create_refresh_token({"sub": str(user.id)})

        expires_at = datetime.now(timezone.utc) + timedelta(days=7)

        await RefreshToken.filter(user=user, revoked=False).update(revoked=True)

        await RefreshToken.create(token=refresh_token, user=user, expires_at=expires_at)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def refresh_token(self, refresh_token: str):
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="invalid refresh token",
                )

            stored_token = await RefreshToken.filter(
                token=refresh_token,
                revoked=False,
            ).first()

            if not stored_token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Refresh token inválido",
                )

            if stored_token.expires_at < datetime.now(timezone.utc):
                await stored_token.delete()

                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Refresh token expirado",
                )

            await RefreshToken.filter(id=stored_token.id).update(revoked=True)

            user_id = payload.get("sub")

            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido",
                )

            new_access_token = create_access_token({"sub": str(user_id)})

            new_refresh_token = create_refresh_token({"sub": str(user_id)})

            expires_at = datetime.now(timezone.utc) + timedelta(days=7)

            await RefreshToken.create(
                token=new_refresh_token,
                user_id=stored_token.user_id,
                expires_at=expires_at,
            )

            return {
                "access_token": new_access_token,
                "refresh_token": new_refresh_token,
                "token_type": "bearer",
            }

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

    async def logout(self, current_user: User):
        await RefreshToken.filter(user=current_user, revoked=False).update(revoked=True)

        return {"message": "Logout realizado com sucesso."}

    async def forgot_password(self, data: ForgotPassword):
        user = await User.filter(email=data.email).first()

        if not user:
            return {
                "message": "Se o email estiver cadastrado, voce receberá um link para redefinir sua senha."
            }

        await PasswordResetToken.filter(
            user=user,
            used_at=None,
        ).update(used_at=datetime.now(timezone.utc))

        token = generate_password_reset_token()

        token_hash = hash_password_reset_token(token)

        expires_at = datetime.now(timezone.utc) + timedelta(minutes=60)

        await PasswordResetToken.create(
            user=user, token_hash=token_hash, expires_at=expires_at
        )

        email_service = EmailService()

        await email_service.send_password_reset_email(
            email=user.email,
            reset_token=token,
        )

        return {
            "message": (
                "Se o email estiver cadastrado, voce receberá um link para redefinicao de senha"
            )
        }

    async def reset_password(self, data: ResetPassword):
        token_hash = hash_password_reset_token(data.token)

        reset_token = (
            await PasswordResetToken.filter(
                token_hash=token_hash,
                used_at=None,
            )
            .prefetch_related("user")
            .first()
        )

        if not reset_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token inválido ou já utilizado.",
            )

        now = datetime.now(timezone.utc)

        if reset_token.expires_at <= now:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token expirado",
            )

        user = reset_token.user

        user.password_hash = hash_password(data.new_password)

        await user.save()

        reset_token.used_at = now

        await reset_token.save(update_fields=["used_at"])

        await (
            PasswordResetToken.filter(
                user=user,
                used_at=None,
            )
            .exclude(id=reset_token.id)
            .update(used_at=now)
        )

        return {"message": "Senha redefinida com sucesso."}
