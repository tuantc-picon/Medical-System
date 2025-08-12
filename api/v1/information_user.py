from fastapi import APIRouter, Depends, status, Query
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from app.users.schemas.user import UserReadSchema
from core.common.database import get_async_db_session
from core.services.information_user import ViewInformation
from core.utils.authorize import authorize_user


view = APIRouter(prefix="", tags=["View"])


@view.get("/users", response_model=List[UserReadSchema], status_code=status.HTTP_200_OK)
async def view_list_users(
    role_id: int = Query(...),
    name: str = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=0),
    db: AsyncSession = Depends(get_async_db_session),
    authorize=Depends(authorize_user("information_list_user:view")),
):
    service = ViewInformation(db=db)
    return await service.list_user(
        offset=offset, limit=limit, name=name, role_id=role_id
    )


@view.get("/user/{user_id}", status_code=status.HTTP_200_OK)
async def view_user_details(
    id: int,
    db: AsyncSession = Depends(get_async_db_session),
):
    service = ViewInformation(db=db)
    return await service.get_user_details(id)


@view.get("/me", status_code=status.HTTP_200_OK)
async def view_user_details(
    authorize=Depends(authorize_user("me:view")),
    db: AsyncSession = Depends(get_async_db_session),
):
    service = ViewInformation(db=db)
    try:
        result = await service.get_me(authorize.id)
        return result
    except Exception as e:
        print("Error in get_me:", e)
        raise
