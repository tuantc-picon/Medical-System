import asyncio
from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError
from pydantic import EmailStr
from sqlalchemy import delete

from app.users.schemas import AccessTokenData
from config import (JWT_ACCESS_SECRET_KEY,
                    JWT_REFRESH_SECRET_KEY,
                    ALGORITHM,
                    ACCESS_TOKEN_EXPIRED,
                    REFRESH_TOKEN_EXPIRED)
from core.common.Base import BaseService
from core.models.token import ListToken
from core.models.user import User
from .number import int_to_datetime
from core.common.database import get_async_db_session


class Token(BaseService):

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
        return Token.create_token(to_encode, JWT_ACCESS_SECRET_KEY, expires_delta=expires)

    @staticmethod
    def create_refresh_token(data: dict):
        to_encode = data.copy()
        to_encode.update({"type": "refresh"})
        expires = timedelta(days=REFRESH_TOKEN_EXPIRED)
        return Token.create_token(to_encode, JWT_REFRESH_SECRET_KEY, expires_delta=expires)

    async def verify_access_token(self, token: str, credentials_exception):
        try:
            payload = jwt.decode(token, JWT_ACCESS_SECRET_KEY, algorithms=[ALGORITHM])
            email: EmailStr = payload.get("subEmail")
            name: str = payload.get("subName")
            role: str = payload.get("role")
            type: str = payload.get("type")
            if type != "access":
                raise credentials_exception

            result_used = await self.fetch_one(ListToken, access_token=token)
            if result_used or result_used.deleted_at:
                raise credentials_exception

            access_token_data = AccessTokenData(email=email, name=name, role=role)
        except JWTError:
            raise credentials_exception
        return access_token_data

    async def verify_refresh_token(self, refreshToken: str, credentials_exception):
        try:
            payload = jwt.decode(refreshToken, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
            email: EmailStr = payload.get("subEmail")
            id: int = payload.get("subID")
            type: str = payload.get("type")
            if type != "refresh":
                raise credentials_exception

            result_used = await self.fetch_one(ListToken, refresh_token=refreshToken)

            if not result_used:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        refresh_token_data = await self.fetch_one(User, id=id, email=email)
        if not refresh_token_data or result_used.deleted_at:
            raise credentials_exception
        return refresh_token_data


    async def clean_expired_token(self):
        expired_delta = timedelta(minutes=REFRESH_TOKEN_EXPIRED)
        while True:
            try:
                async for session in get_async_db_session():
                    now = datetime.now(timezone.utc)
                    await session.execute(
                        delete(ListToken).where(
                            ListToken.created_at < now - expired_delta
                        )
                    )
                    await session.commit()
                    break
            except Exception as e:
                print(f"[clean_expired_token] Error: {e}")
            await asyncio.sleep(3600)
