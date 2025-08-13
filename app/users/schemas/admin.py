from typing import Optional

from datetime import datetime


from .user import UserCreateSchema, UserBaseSchema


class AdminBaseSchema(UserBaseSchema):
    phone_number: Optional[str]=None
    address: Optional[str]=None


class AdminCreateSchema(UserCreateSchema):
    pass

class AdminReadSchema(AdminBaseSchema):
    created_at: datetime
    updated_at: Optional[datetime]=None


class AdminUpdateSchema:
    phone_number: Optional[str]
    address: Optional[str]