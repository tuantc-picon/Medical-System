from aiohttp import payload_type
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.users import schemas
from datetime import datetime, timedelta
from config import (JWT_ACCESS_SECRET_KEY,
                    JWT_REFRESH_SECRET_KEY,
                    ALGORITHM,
                    ACCESS_TOKEN_EXPIRED,
                    REFRESH_TOKEN_EXPIRED)
from pydantic import EmailStr
from app.users.schemas import TokenData

def create_token(data: dict, secret_key, algorithms, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode( to_encode, secret_key, algorithm=algorithms)
    return encoded_jwt


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"type": "access"})
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRED)
    return create_token(to_encode, JWT_ACCESS_SECRET_KEY, ALGORITHM, expires_delta=expires)


def create_refresh_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"type": "refresh"})
    expires = timedelta(days=REFRESH_TOKEN_EXPIRED)
    return create_token(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM, expires_delta=expires)


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, JWT_ACCESS_SECRET_KEY, algorithms=[ALGORITHM])
        email : EmailStr = payload.get("subEmail")
        name: str = payload.get("subName")
        if email or name is None:
            raise credentials_exception
        token_data = TokenData(email=email, name=name)
    except JWTError:
        raise credentials_exception
    return token_data