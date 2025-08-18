from fastapi import APIRouter, Depends, status, Query
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from app.users.schemas.user import UserReadSchema
from core.common.database import get_async_db_session
from app.users.schemas.user import UserListQuerySchema
from core.services.user import UserService
from core.utils.authorize import authorize_user


user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.get(
    "", response_model=List[UserReadSchema], status_code=status.HTTP_200_OK
)
async def get_users_list(
    user_information=Depends(UserListQuerySchema),
    db_session: AsyncSession = Depends(get_async_db_session),
    authorized_user=Depends(authorize_user("information_list_user:view")),
):
    user_service = UserService(db=db_session)
    return await user_service.get_user_list(user_information)


@user_router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_detail(
    user_id: int,
    db_session: AsyncSession = Depends(get_async_db_session),
    authorized=Depends(authorize_user("information_user:search")),
):
    user_service = UserService(db=db_session)
    return await user_service.get_user_detail(user_id)
