from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_403_FORBIDDEN

from core.common.database import get_async_db_session
from core.models.role import Permission, RolePermission
from core.services.bearer import authenticate_token
from sqlalchemy import select


def authorize_user(permission_name: str) :
    async def check_permission(
            current_user=Depends(authenticate_token),
            db: AsyncSession = Depends(get_async_db_session)):
        try:
            user_role_id = current_user.role_id
            permission= (
                            await db.execute(
                                            select(Permission).where(Permission.name == permission_name)
                            )
                         ).scalar_one_or_none()

            if not permission:
                raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=f"Permission '{permission_name}' not found")

            role_permission = (
                await db.execute(
                    select(RolePermission).where(
                        RolePermission.role_id == user_role_id,
                        RolePermission.permission_id == permission.id
                    )
                )
            ).scalar_one_or_none()

            if not role_permission:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="do not have permission to perform this action"
                )

            return True
        except SQLAlchemyError as e:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    return check_permission



