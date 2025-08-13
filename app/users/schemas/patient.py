from typing import Optional

from .user import UserCreateSchema, UserBaseSchema
from datetime import datetime


class PatientBaseSchema(UserBaseSchema):
    job: Optional[str]=None
    insurance_number: Optional[str]=None


class PatientCreateSchema(UserCreateSchema):
    pass


class PatientUpdateSchema:
    job: Optional[str] = None
    insurance_number: Optional[str] = None


class PatientReadSchema(PatientBaseSchema):
    created_at: datetime
    updated_at: Optional[datetime]=None
