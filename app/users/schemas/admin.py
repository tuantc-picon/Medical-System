from typing import Optional

from core.schemas.base import MSBaseSchema, MSTimestamp
from .user import UserCreateSchema, UserBaseSchema


class AdminBaseSchema(MSBaseSchema):
    phone_number: Optional[str]=None
    address: Optional[str]=None


class AdminCreateSchema(UserCreateSchema, AdminBaseSchema):
    pass


class AdminReadSchema(UserBaseSchema,AdminBaseSchema):
    created_at: MSTimestamp
    updated_at: MSTimestamp


class AdminUpdateSchema():
    phone_number: Optional[str]
    address: Optional[str]