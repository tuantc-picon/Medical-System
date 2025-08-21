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

            stmt_users = select(User)
            stmt_count = select(func.count()).select_from(User)

            if conditions:
                stmt_users = stmt_users.where(and_(*conditions))
                stmt_count = stmt_count.where(and_(*conditions))
            result_count = await self.db.execute(stmt_count)
            total_users = result_count.scalar_one()

            pagination = MSPaginationBaseSchema(
                page=user_information.page,
                limit_page=user_information.limit_page,
                no_pagination=user_information.no_pagination,
            )

            base_url = str(request.url).split("?")[0]

            result = await self.fetch_pagination(
                stmt_users,
                pagination,
                base_url,
                total_users,
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