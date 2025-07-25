from .user import UserBase, UserUpdate, UserCreate
from . import MSTimestamp, MSBaseSchema, RoleEnum
from typing import Optional

class DoctorBase(MSBaseSchema):
    pass

class DoctorCreate(UserCreate):
    specialization: str
    graduated_at: str

class DoctorRead(DoctorBase):
    created_at: MSTimestamp
    updated_at: MSTimestamp

class DoctorUpdate():
    specialization: Optional[str]
    graduated_at: Optional[str]