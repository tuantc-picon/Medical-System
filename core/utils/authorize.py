from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_403_FORBIDDEN

from core.common.database import get_async_db_session
from core.models.role import Permission, RolePermission
from core.utils.bearer import validate_token
from sqlalchemy import select


def authorize_user(permission_name: str) :
    async def check_permission(
            current_user=Depends(validate_token),
            db: AsyncSession = Depends(get_async_db_session)):
        try:

            result = await db.execute(
                select(RolePermission)
                .join(Permission, Permission.id == RolePermission.permission_id)
                .where(
                    RolePermission.role_id == current_user.role_id,
                    Permission.name == permission_name
                )
            )

            role_permission = result.scalar_one_or_none()

            if not role_permission:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="do not have permission to perform this action"
                )


            return current_user
        except SQLAlchemyError as e:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    return check_permission



