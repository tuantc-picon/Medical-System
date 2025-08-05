from fastapi import APIRouter, status, Depends
from app.users.schemas.role import RoleMenuPermissionCreate
from sqlalchemy.ext.asyncio import AsyncSession
from core.common.database import get_async_db_session
from core.services.role import RoleService

role = APIRouter(
    prefix="/v1/role",
    tags=["Role"],
)


@role.post("/add", response_model=RoleMenuPermissionCreate, status_code=status.HTTP_201_CREATED)
async def assign_role_permission(data: RoleMenuPermissionCreate, db: AsyncSession = Depends(get_async_db_session)):
    service = RoleService(db)
    return await service.assign_role_permission(data)
