from . import MSTimestamp, MSBaseSchema
from typing import Optional
from .user import UserCreate

class AdminBase(MSBaseSchema):
    pass

class AdminCreate(UserCreate):
    phone_number: str
    address: str

class AdminRead(AdminBase):
    created_at: MSTimestamp
    updated_at: MSTimestamp

class AdminUpdate():
    phone_number: Optional[str]
    address: Optional[str]