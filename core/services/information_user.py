from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status


from app.users.schemas.user import UserReadSchema
from core.common.Base import BaseService
from typing import Optional

from core.common.mapping import ROLE_MAPPING_READ
from core.models.user import User



class ViewInformation(BaseService):
    async def get_list_user(self,
                        offset: int,
                        limit: int,
                        name: Optional[str] = None,
                        role_id: Optional[int] = None):
        try:
            conditions = []
            if name is not None:
                conditions.append(User.name.ilike(f"%{name}%"))
            if role_id is not None:
                conditions.append(User.role_id == role_id)
            users = await self.fetch_all(User, offset=offset, limit=limit, conditions=conditions)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        return [UserReadSchema.model_validate(user) for user in users]


    async def get_user_details(
            self,
            id: int,
    ):
        user = await self.fetch_one(User, id=id)
        schema_cls = ROLE_MAPPING_READ(user.role_id)
        information_detail = schema_cls.model_validate(user)
        return information_detail


    async def get_me(self, id: int):
        return await self.get_user_details(id=id)