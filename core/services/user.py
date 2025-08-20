from pydantic import HttpUrl
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy import select, and_
from fastapi import HTTPException, status

from app.users.schemas.user import UserListReadSchema
from core.common.Base import BaseService, MSPaginationBaseSchema

from core.common.mapping import ROLE_MAPPING_READ_SCHEMA
from core.models.user import User
from app.users.schemas.user import UserListQuerySchema






class UserService(BaseService):
    async def get_user_list(self, user_information: UserListQuerySchema, base_url: HttpUrl):
        try:
            conditions = []
            if user_information.name:
                conditions.append(User. name.ilike(f"%{user_information.name}%"))
            if user_information.role_id:
                conditions.append(User.role_id == user_information.role_id)

            stmt = select(User)
            if conditions:
                stmt = stmt.where(and_(*conditions))

            pagination_data = MSPaginationBaseSchema(page=user_information.page,
                                                     limit=user_information.limit,
                                                     no_pagination=user_information.no_pagination)
            users = await self.fetch_pagination(stmt,base_url, UserListReadSchema,  pagination_data)
            return users
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def get_user_detail(
            self,
            id: int,
    ):
        user = await self.fetch_one(User, id=id)
        schema_cls = ROLE_MAPPING_READ_SCHEMA.get(user.role_id)
        information_detail = schema_cls.model_validate(user)
        return information_detail