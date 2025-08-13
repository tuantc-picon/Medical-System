from fastapi import APIRouter, status, HTTPException

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.schemas.user import UserLoginSchema
from core.common.database import get_async_db_session
from core.services.authention import AuthentionService
from core.utils.bearer import get_access_token
from core.services.view_information import ViewInformationService
from core.utils.authorize import authorize_user

authentication = APIRouter(prefix="/auth", tags=["Authentication"])


@authentication.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    request: UserLoginSchema,
    db: AsyncSession = Depends(get_async_db_session),
):
    auth_service = AuthentionService(db)
    return await auth_service.login_user(request)


@authentication.get("/logout", status_code=status.HTTP_200_OK)
async def logout_user(
    access_token=Depends(get_access_token),
    db: AsyncSession = Depends(get_async_db_session),
):
    auth_service = AuthentionService(db)
    return await auth_service.logout_user(access_token)


@authentication.post("/refresh", status_code=status.HTTP_200_OK)
async def renew_token(
    refresh_access_token: str, db: AsyncSession = Depends(get_async_db_session)
):
    auth_service = AuthentionService(db)
    return await auth_service.renew_token(refresh_access_token)


@authentication.get("/me", status_code=status.HTTP_200_OK)
async def view_me(
    authorize=Depends(authorize_user("me:view")),
    db_session: AsyncSession = Depends(get_async_db_session),
):
    view_service = ViewInformationService(db=db_session)
    try:
        return await view_service.get_user_detail(authorize.id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
