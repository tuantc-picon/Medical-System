from . import MSBaseSchema, MSTimestamp
from pydantic import EmailStr
from core.common.constants import RoleEnum

class Token(MSBaseSchema):
    access_token: str
    token_type: str

class TokenData(MSBaseSchema):
    email: EmailStr
    name: str
    role: RoleEnum