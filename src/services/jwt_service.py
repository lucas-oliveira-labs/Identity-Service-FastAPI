from datetime import datetime, timedelta, timezone
from jose import jwt
from src.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict):
    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload.update({"exp": expire, "type": "access"})

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(days=7)

    payload.update({"exp": expire, "type": "refresh"})

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
