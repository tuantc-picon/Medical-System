from datetime import datetime, timedelta
from fastapi import HTTPException, status

from jose import jwt, JWTError
from pydantic import EmailStr

from app.users.schemas.token import AccessTokenDataSchema
from config import (JWT_ACCESS_SECRET_KEY,
                    JWT_REFRESH_SECRET_KEY,
                    ALGORITHM,
                    ACCESS_TOKEN_EXPIRED,
                    REFRESH_TOKEN_EXPIRED)
from core.common.Base import BaseService
from core.models.token import ListToken
from core.models.user import User


class TokenService(BaseService):

    @staticmethod
    def create_token(data: dict, secret_key, expires_delta: timedelta = None, algorithms=ALGORITHM):
        if expires_delta is None:
            expires_delta = timedelta(minutes=15)
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithms)
        return encoded_jwt

    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        to_encode.update({"type": "access"})
        expires = timedelta(days=ACCESS_TOKEN_EXPIRED)
        return TokenService.create_token(to_encode, JWT_ACCESS_SECRET_KEY, expires_delta=expires)

    @staticmethod
    def create_refresh_token(data: dict):
        to_encode = data.copy()
        to_encode.update({"type": "refresh"})
        expires = timedelta(days=REFRESH_TOKEN_EXPIRED)
        return TokenService.create_token(to_encode, JWT_REFRESH_SECRET_KEY, expires_delta=expires)

    async def verify_access_token(self, token: str):
        try:
            payload = jwt.decode(token, JWT_ACCESS_SECRET_KEY, algorithms=[ALGORITHM])
            email: EmailStr = payload.get("subEmail")
            name: str = payload.get("subName")
            role_id: int = payload.get("role_id")
            type: str = payload.get("type")
            if type != "access":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            result_used = await self.fetch_one(ListToken, access_token=token)
            if not result_used or result_used.deleted_at:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            access_token_data = AccessTokenDataSchema(email=email, name=name, role_id=role_id)
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return access_token_data

    async def verify_refresh_token(self, refreshToken: str):
        try:
            payload = jwt.decode(refreshToken, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
            email: EmailStr = payload.get("subEmail")
            id: int = payload.get("subID")
            type: str = payload.get("type")
            if type != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            result_used = await self.fetch_one(ListToken, refresh_token=refreshToken)

            if not result_used:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        refresh_token_data = await self.fetch_one(User, id=id, email=email)
        if not refresh_token_data or result_used.deleted_at:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return refresh_token_data
