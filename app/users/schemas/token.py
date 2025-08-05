from pydantic import EmailStr

from . import MSBaseSchema


class TokenSchema(MSBaseSchema):
    access_token: str
    token_type: str


class AccessTokenDataSchema(MSBaseSchema):
    email: EmailStr
    name: str
    role_id: int


class RefreshTokenDataSchema(MSBaseSchema):
    email: EmailStr
    id: int
