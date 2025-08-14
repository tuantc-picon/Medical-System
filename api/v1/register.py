from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.schemas.user import UserCreateSchema, UserResponseSchema
from core.services.register import RegisterService
from . import get_async_db_session
from core.common.mapping import ROLE_MAPPING_REGISTER_SCHEMA

register = APIRouter(prefix="/register", tags=["Register"])


@register.post(
    "",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    data: UserCreateSchema,
    db: AsyncSession = Depends(get_async_db_session),
):
    register_service = RegisterService(db)

    if data.role_id not in ROLE_MAPPING_REGISTER_SCHEMA:
        raise HTTPException(status_code=400, detail="Invalid role")
    return await register_service.register_user_information(data)
