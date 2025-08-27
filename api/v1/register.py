from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.schemas.user import UserCreateSchema, UserResponseSchema
from core.services.register import RegisterService
from . import get_async_db_session

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
    return await register_service.register_user_information(data)
