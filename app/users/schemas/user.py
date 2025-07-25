from . import MSBaseSchema, MSTimestamp
from . import GenderEnum, RoleEnum
from typing import Optional
from pydantic import EmailStr

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