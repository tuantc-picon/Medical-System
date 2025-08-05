from fastapi import Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_403_FORBIDDEN

from core.common.database import get_async_db_session
from core.models.role import Menu, RoleMenu
from core.services.oauth2 import authenticate_token
from sqlalchemy import select


async def authorize_user(
        request: Request,
        current_user=Depends(authenticate_token),
        db: AsyncSession = Depends(get_async_db_session)):
    path = request.url.path
    method = request.method.upper()

    menu_query = await db.execute(select(Menu).where(Menu.path == path))
    menu = menu_query.scalar_one_or_none()
    if not menu:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid request")

    role_menu_query = await db.execute(
        select(RoleMenu).where(
            RoleMenu.role_id == current_user.role_id,
            RoleMenu.menu_id == menu.id
        )
    )

    role_menu = role_menu_query.scalar_one_or_none()
    if not role_menu or method not in role_menu.list_method:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Without permission")

    return True
