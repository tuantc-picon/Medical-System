from sqlalchemy import select
from core.models.role import Role
from core.common.constants import DEFAULT_ROLES
from core.common.database import get_async_db_session
from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError


async def init_roles():
    try:
        async for session in get_async_db_session():
            result = await session.execute(select(Role))
            existing_roles = result.scalars().all()
            if existing_roles:
                return
            for role in DEFAULT_ROLES:
                session.add(Role(id=role["id"], name=role["name"]))
            await session.commit()
    except SQLAlchemyError as e:
        print(f"Error initializing roles: {e}")
