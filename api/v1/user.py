from fastapi import APIRouter, Depends, status, Query
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from app.users.schemas.user import UserReadSchema
from core.common.database import get_async_db_session
from core.services.view_information import ViewInformationService
from core.utils.authorize import authorize_user


user = APIRouter(prefix="/users", tags=["User"])


@user.get("", response_model=List[UserReadSchema], status_code=status.HTTP_200_OK)
async def view_users_list(
    role_id: int = Query(None),
    name: str = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=0),
    db_session: AsyncSession = Depends(get_async_db_session),
    authorize=Depends(authorize_user("information_list_user:view")),
):
    view_service = ViewInformationService(db=db_session)
    return await view_service.get_user_list(
        offset=offset, limit=limit, name=name, role_id=role_id
    )


@user.get("/{user_id}", status_code=status.HTTP_200_OK)
async def view_user_detail(
    user_id: int,
    db_session: AsyncSession = Depends(get_async_db_session),
    authorize=Depends(authorize_user("information_user:search")),
):
    view_service = ViewInformationService(db=db_session)
    return await view_service.get_user_detail(user_id)
