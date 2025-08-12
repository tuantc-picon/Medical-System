from typing import Optional


from pydantic import EmailStr

from core.common.constants import GenderEnum
from core.schemas.base import MSBaseSchema, MSTimestamp


class UserBaseSchema(MSBaseSchema):
    name: str
    email: EmailStr
    gender: GenderEnum
    role_id: int
    age: Optional[int] = None


class UserCreateSchema(UserBaseSchema):
    password: str
    extra_fields: dict

class UserResponseSchema(UserBaseSchema):
    id: int
    extra_fields: dict

class UserReadSchema(UserBaseSchema):
    created_at: MSTimestamp
    updated_at: MSTimestamp


class UserUpdateSchema(MSBaseSchema):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    gender: Optional[GenderEnum] = None
    age: Optional[int] = None
    password: str


class UserLoginSchema(MSBaseSchema):
    email: EmailStr
    password: str
