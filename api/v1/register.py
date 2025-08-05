from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.schemas.admin import AdminCreateSchema
from app.users.schemas.doctor import DoctorCreateSchema
from app.users.schemas.patient import PatientCreateSchema
from app.users.schemas.user import UserCreateSchema, UserResponseSchema
from core.common.constants import DefaultRoleEnum
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
    service = RegisterService(db)

    role_mapping = {
        DefaultRoleEnum.ADMIN.role_id: (AdminCreateSchema, service.register_admin),
        DefaultRoleEnum.DOCTOR.role_id: (DoctorCreateSchema, service.register_doctor),
        DefaultRoleEnum.PATIENT.role_id: (
            PatientCreateSchema,
            service.register_patient,
        ),
    }

    if data.role_id not in role_mapping:
        raise HTTPException(status_code=400, detail="Invalid role")

    schema_class, service_method = role_mapping[data.role_id]
    user = schema_class(**data.dict())
    return await service_method(user)
