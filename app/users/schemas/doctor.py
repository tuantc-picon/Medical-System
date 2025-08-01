from typing import Optional

from . import MSTimestamp, MSBaseSchema
from .user import UserCreate


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
