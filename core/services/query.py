from sqlalchemy import select
from core.models.user import User
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from core.utils.hashing import Hash

class verify:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def db(self, email:EmailStr, name: str):
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            return False
        if user.name != name:
            return False
        return True

    async def authention(self,username,password, role):
        stmt = select(User).where(User.email == username)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()
        if not user or not Hash.verify(password, user.password) or user.role != role:
            return None
        return user