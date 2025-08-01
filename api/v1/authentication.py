from fastapi import APIRouter
# from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.schemas.user import UserLogin
from core.common.database import get_async_db_session
from core.services.authention import AuthentionService

Login = APIRouter(
    tags=["authentication"]
)


@Login.post("/login")
async def login(request: UserLogin, db: AsyncSession = Depends(get_async_db_session)):
    auth_service = AuthentionService(db)
    return await auth_service.login(request)


@Login.post("/logout")
async def logout(access_token: str, refresh_access_token: str, db: AsyncSession = Depends(get_async_db_session)):
    auth_service = AuthentionService(db)
    return await auth_service.logout(access_token, refresh_access_token)


@Login.post("/refresh")
async def refresh_token(refresh_access_token: str, db: AsyncSession = Depends(get_async_db_session)):
    auth_service = AuthentionService(db)
    return await auth_service.refresh_token(refresh_access_token)
