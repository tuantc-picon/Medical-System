from fastapi import HTTPException, status
from core.common.Base import BaseService
from sqlalchemy.exc import SQLAlchemyError
from core.models.role import Role, Menu, RoleMenu
from app.users.schemas.role import RoleMenuPermissionCreate


class RoleService(BaseService):
    async def assign_role_permission(self, data: RoleMenuPermissionCreate):
        try:
            # 1. check for role existence
            role_obj = await self.fetch_one(Role, id=data.role_id)
            if not role_obj:
                raise HTTPException(status_code=404, detail="Role not found.")

            # 2. find or create Menu by path
            menu_obj = await self.fetch_one(Menu, path=data.menu_path)
            if not menu_obj:
                menu_obj = Menu(path=data.menu_path)
                self.db.add(menu_obj)
                await self.db.flush()
                await self.db.refresh(menu_obj)

            # 3. find or create RoleMenu
            role_menu_obj = await self.fetch_one(RoleMenu, role_id=data.role_id, menu_id=menu_obj.id)
            if role_menu_obj:
                role_menu_obj.list_method = data.methods
                await self._save(role_menu_obj)  # can commit when update
            else:
                role_menu_obj = RoleMenu(
                    role_id=data.role_id,
                    menu_id=menu_obj.id,
                    list_method=data.methods
                )
                await self._save(role_menu_obj)

        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )
        return RoleMenuPermissionCreate(
            role_id=data.role_id,
            menu_path=data.menu_path,
            methods=data.methods)
