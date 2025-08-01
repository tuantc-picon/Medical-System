from pydantic import EmailStr

from . import MSBaseSchema


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
