from typing import Optional
from datetime import datetime

from .user import UserCreateSchema, UserBaseSchema


class DoctorBaseSchema(UserBaseSchema):
    specialization: Optional[str]= None
    graduated_at: Optional[str]= None



class DoctorCreateSchema(UserCreateSchema):
    pass

class DoctorReadSchema(DoctorBaseSchema):
    created_at: datetime
    updated_at: Optional[datetime]=None

class DoctorUpdateSchema():
    specialization: Optional[str]
    graduated_at: Optional[str]
