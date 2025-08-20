from fastapi import APIRouter, Depends, status, Request

from sqlalchemy.ext.asyncio import AsyncSession
from app.users.schemas.user import UserListQuerySchema
from core.common.database import get_async_db_session
from core.services.user import UserService
from core.utils.authorize import authorize_user


user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.get("", status_code=status.HTTP_200_OK)
async def get_users_list(
    request: Request,
    query_schema=Depends(UserListQuerySchema),
    db_session: AsyncSession = Depends(get_async_db_session),
    authorized_user=Depends(authorize_user("user:view-list")),
):
    base_url = str(request.url).split("?")[0]

    user_service = UserService(db=db_session)
    return await user_service.get_user_list(query_schema, base_url)


@user_router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_detail(
    user_id: int,
    db_session: AsyncSession = Depends(get_async_db_session),
    authorized=Depends(authorize_user("user:view-detail")),
):
    user_service = UserService(db=db_session)
    return await user_service.get_user_detail(user_id)
