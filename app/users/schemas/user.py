from typing import Optional
from datetime import datetime

from pydantic import EmailStr, field_serializer

from core.common.constants import GenderEnum
from core.schemas.base import MSBaseSchema, MSSortPaginationBaseSchema

class UserBaseSchema(MSBaseSchema):
    name: str
    email: EmailStr
    gender: int = GenderEnum.OTHER.gender_id
    role_id: int
    age: Optional[int] = None
    @field_serializer("gender")
    def gender_to_str(self, gender: int):
        return GenderEnum(gender).gender_name


class UserCreateSchema(UserBaseSchema):
    password: str
    extra_fields: dict


class UserBaseResponseSchema(UserBaseSchema):
    id: int

class UserResponseSchema(UserBaseResponseSchema):
    extra_fields: dict

class UserReadSchema(UserBaseSchema):
    created_at: datetime
    updated_at: Optional[datetime]=None

class UserUpdateSchema(MSBaseSchema):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    gender: Optional[GenderEnum] = None
    age: Optional[int] = None
    password: str


class UserLoginSchema(MSBaseSchema):
    email: EmailStr
    password: str


class UserListQuerySchema(MSSortPaginationBaseSchema):
    role_id: Optional[int] = None
    name: Optional[str] = None