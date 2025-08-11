from typing import Optional

from core.schemas.base import MSBaseSchema, MSTimestamp
from .user import UserCreateSchema, UserBaseSchema


class DoctorBaseSchema(MSBaseSchema):
    specialization: Optional[str]= None
    graduated_at: Optional[str]= None


class DoctorCreateSchema(UserCreateSchema, DoctorBaseSchema):
    pass


class DoctorReadSchema(UserBaseSchema,DoctorBaseSchema):
    created_at: MSTimestamp
    updated_at: MSTimestamp


class DoctorUpdateSchema():
    specialization: Optional[str]
    graduated_at: Optional[str]
