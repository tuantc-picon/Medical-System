from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models.user import User
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from core.utils.hashing import Hash

from core.common.constants import RoleEnum  # nếu bạn dùng Enum như vậy

async def verify_db(email: EmailStr, name: str, role: str, db: AsyncSession):
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        return False
    if user.name.strip().lower() != name.strip().lower():
        return False
    if isinstance(user.role, RoleEnum):
        user_role = user.role.value  # Lấy ra string từ Enum
    else:
        user_role = str(user.role)
    if user_role != role:
        return False
    return True


async def verify_authention(username: str, password: str, role: RoleEnum, db: AsyncSession):
    stmt = select(User).where(User.email == username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        return None
    if not Hash.verify(password, user.password):
        return None
    if user.role != role:
        return None
    return user
