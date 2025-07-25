from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models.user import User
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from core.utils.hashing import Hash

async def verify_db(email:EmailStr, name: str, db: AsyncSession):
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        return False
    if user.name != name:
        return False
    return True

async def verify_authention(username,password, db: AsyncSession):
    stmt = select(User).where(User.email == username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user or not Hash.verify(password, user.password):
        return False
    return True