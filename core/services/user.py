from fastapi import Request
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy import select, and_, func
from fastapi import HTTPException, status

from core.common.Base import BaseService, MSPaginationBaseSchema

from core.common.mapping import ROLE_MAPPING_READ_SCHEMA
from core.models.user import User
from app.users.schemas.user import UserListQuerySchema, UserBaseResponseSchema


class UserService(BaseService):
    async def get_user_list(self, user_information: UserListQuerySchema, request):
        try:
            conditions = []
            if user_information.name:
                conditions.append(User.name.ilike(f"%{user_information.name}%"))
            if user_information.role_id:
                conditions.append(User.role_id == user_information.role_id)
            data = user_information.model_dump() # use model_dump() instead of dict()

            stmt = select(User,func.count().label("total")).group_by(User.id)
            stmt = stmt.where(*conditions)

            base_url = str(request.url).split("?")[0]
            data["base_url"] = base_url

            result = await self.fetch_pagination(
                stmt,
                data,
                UserBaseResponseSchema,
            )
            return result

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