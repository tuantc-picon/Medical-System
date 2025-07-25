from .doctor import DoctorRead, DoctorBase
from .user import UserBase, UserUpdate, UserCreate
from . import MSBaseSchema, MSTimestamp
from typing import Optional

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