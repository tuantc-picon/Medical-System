from fastapi import APIRouter, status, Response

# from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.schemas.user import UserLogin
from core.common.database import get_async_db_session
from core.services.authention import AuthentionService

authentication = APIRouter(prefix="/v1", tags=["Authentication"])


@authentication.post("/login", status_code=status.HTTP_202_ACCEPTED)
async def login(
    request: UserLogin,
    db: AsyncSession = Depends(get_async_db_session),
):
    auth_service = AuthentionService(db)
    return await auth_service.login(request)


@authentication.post("/logout", status_code=status.HTTP_202_ACCEPTED)
async def logout(
    access_token: str,
    refresh_access_token: str,
    db: AsyncSession = Depends(get_async_db_session),
):
    auth_service = AuthentionService(db)
    return await auth_service.logout(access_token, refresh_access_token)


@authentication.post("/refresh", status_code=status.HTTP_202_ACCEPTED)
async def refresh_token(
    refresh_access_token: str, db: AsyncSession = Depends(get_async_db_session)
):
    auth_service = AuthentionService(db)
    return await auth_service.refresh_token(refresh_access_token)
