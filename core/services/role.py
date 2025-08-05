from fastapi import HTTPException, status
from core.common.Base import BaseService
from sqlalchemy.exc import SQLAlchemyError
from core.models.role import Role, Permission, RolePermission
from app.users.schemas.role import (
    RolePermissionCreateSchema,
    RolePermissionReadSchema,
)


class RoleService(BaseService):

    async def assign_role_permission(self, data: RolePermissionCreateSchema):
        try:
            # Check if role exists
            role = await self.fetch_one(Role, id=data.role_id)
            if not role:
                raise HTTPException(status_code=404, detail="Role not found.")

            # Check if permission exists
            permission = await self.fetch_one(Permission, name=data.name)
            if not permission:
                permission = Permission(name=data.name)
                self.db.add(permission)
                await self.db.flush()
                await self.db.refresh(permission)

            # if not permission in role => create RolePermission
            role_permission = await self.fetch_one(
                RolePermission, role_id=data.role_id, permission_id=permission.id
            )

            if not role_permission:
                role_permission = RolePermission(
                    role_id=data.role_id,
                    permission_id=permission.id,
                )

            data_return = RolePermissionReadSchema(
                role_id=data.role_id,
                permission_id=role_permission.permission_id,
                name=data.name,
            )
            await self._save(role_permission)

            return data_return

        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}",
            )

        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}",
            )
