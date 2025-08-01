from typing import Optional

from . import MSBaseSchema, MSTimestamp
from .user import UserCreate


class PatientBase(MSBaseSchema):
    pass


class PatientCreate(UserCreate):
    job: str
    insurance_number: str


class PatientUpdate():
    job: Optional[str]
    insurance_number: Optional[str]


class PatientRead(PatientBase):
    created_at: MSTimestamp
    updated_at: MSTimestamp
