from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models.user import User
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from core.utils.hashing import Hash
from core.common.constants import RoleEnum


async def verify_db(email: EmailStr, name: str, role: str, db: AsyncSession):
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        print("[DEBUG] User not found")
        return False
    if user.name.strip().lower() != name.strip().lower():
        print(f"[DEBUG] Name mismatch: {user.name=} vs {name=}")
        return False
    if isinstance(user.role, RoleEnum):
        user_role = user.role.value  # Lấy ra string từ Enum
    else:
        user_role = str(user.role)
    if user_role != role:
        print(f"[DEBUG] Role mismatch: {user_role=} vs {role=}")
        return False
    return True

async def verify_authention(username,password, db : AsyncSession):
    stmt = select(User).where(User.email == username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None or Hash.verify(password, user.password) is False:
        return None
    return user