from typing import Optional

from pydantic import EmailStr

from core.common.constants import GenderEnum
from core.schemas.base import MSBaseSchema, MSTimestamp


class UserBase(MSBaseSchema):
    name: str
    email: EmailStr
    gender: GenderEnum
    age: Optional[int] = None


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    created_at: MSTimestamp
    updated_at: MSTimestamp


class UserUpdate(MSBaseSchema):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    gender: Optional[GenderEnum] = None
    age: Optional[int] = None
    password: str


class UserLogin(MSBaseSchema):
    email: EmailStr
    password: str
