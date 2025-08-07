from fastapi import Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from core.common.database import get_async_db_session
from core.utils.token import Token

bearer_scheme = HTTPBearer()


async def authenticate_token(
    credential: HTTPAuthorizationCredentials = Security(bearer_scheme),
    db: AsyncSession = Depends(get_async_db_session),
):
    token = credential.credentials
    service = Token(db)
    return await service.verify_access_token(token)
