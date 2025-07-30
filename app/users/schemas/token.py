from . import MSBaseSchema, MSTimestamp
from pydantic import EmailStr

class Token(MSBaseSchema):
    access_token: str
    token_type: str

class AccessTokenData(MSBaseSchema):
    email: EmailStr
    name: str
    role: str

class RefreshTokenData(MSBaseSchema):
    email: EmailStr
    id: int