from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError

from src.services.jwt_service import decode_token
from src.models.user import User
from passlib.context import CryptContext


security = HTTPBearer()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        payload = decode_token(credentials.credentials)

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="invalid token")

        user = await User.filter(id=user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)
