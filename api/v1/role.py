from fastapi import APIRouter, status, Depends
from app.users.schemas.role import RolePermissionCreateSchema
from sqlalchemy.ext.asyncio import AsyncSession
from core.common.database import get_async_db_session
from core.services.role import RoleService

role = APIRouter(
    tags=["Role"],
)


@role.post("", status_code=status.HTTP_201_CREATED)
async def assign_role_permission(
    data: RolePermissionCreateSchema,
    db: AsyncSession = Depends(get_async_db_session),
):
    service = RoleService(db)
    return await service.assign_role_permission(data)
