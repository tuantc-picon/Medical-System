from fastapi import Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from core.common.database import get_async_db_session
from core.services.token import TokenService

bearer_scheme = HTTPBearer()


async def get_access_token(
    credential: HTTPAuthorizationCredentials = Security(bearer_scheme),
):
    return credential.credentials


async def validate_token(
    credential: HTTPAuthorizationCredentials = Security(bearer_scheme),
    db: AsyncSession = Depends(get_async_db_session),
):
    token = await get_access_token(credential)
    service = TokenService(db)
    return await service.verify_access_token(token)
