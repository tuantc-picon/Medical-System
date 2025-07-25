from jose import jwt, JWTError

from datetime import datetime, timedelta

from config import (JWT_ACCESS_SECRET_KEY,
                    JWT_REFRESH_SECRET_KEY,
                    ALGORITHM,
                    ACCESS_TOKEN_EXPIRED,
                    REFRESH_TOKEN_EXPIRED)

from pydantic import EmailStr

from app.users.schemas import TokenData
from core.services.query import verify_db
from sqlalchemy.ext.asyncio import AsyncSession



def create_token(data: dict, secret_key, expires_delta: timedelta = None,  algorithms=ALGORITHM,):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode( to_encode, secret_key, algorithm=algorithms)
    return encoded_jwt


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"type": "access"})
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRED)
    return create_token(to_encode, JWT_ACCESS_SECRET_KEY, expires_delta=expires)


def create_refresh_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"type": "refresh"})
    expires = timedelta(days=REFRESH_TOKEN_EXPIRED)
    return create_token(to_encode, JWT_REFRESH_SECRET_KEY, expires_delta=expires)


async def verify_token(token: str, credentials_exception, db: AsyncSession):
    try:
        payload = jwt.decode(token, JWT_ACCESS_SECRET_KEY, algorithms=[ALGORITHM])
        email : EmailStr = payload.get("subEmail")
        name: str = payload.get("subName")
        role : str = payload.get("role")
        if not await verify_db(email, name, role, db):
            raise credentials_exception
        token_data = TokenData(email=email, name=name, role = role)
    except JWTError:
        raise credentials_exception
    return token_data