from typing import Optional

from core.schemas.base import MSBaseSchema, MSTimestamp
from .user import UserCreateSchema, UserBaseSchema


class PatientBaseSchema(MSBaseSchema):
    job: Optional[str]=None
    insurance_number: Optional[str]=None


class PatientCreateSchema(UserCreateSchema, PatientBaseSchema):
    pass


class PatientUpdateSchema():
    job: Optional[str]
    insurance_number: Optional[str]


class PatientReadSchema(UserBaseSchema,PatientBaseSchema):
    created_at: MSTimestamp
    updated_at: MSTimestamp


