from sqlalchemy import select

from core.common.Base import BaseService
from core.models.user import User
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from core.utils.hashing import Hash

class UserValidator(BaseService):
    pass
    # async def verify_email_name_match(self, email:EmailStr, name: str):
    #     query = select(User).where(User.email == email)
    #     result = await self.db.execute(query)
    #     user = result.scalar_one_or_none()
    #     if not user:
    #         return False
    #     if user.name != name:
    #         return False
    #     return True

    # async def authenticate_user(self,username,password):
    #     stmt = select(User).where(User.email == username)
    #     result = await self.db.execute(stmt)
    #     user = result.scalar_one_or_none()
    #     if not user or not Hash.verify(password, user.password):
    #         return None
    #     return user