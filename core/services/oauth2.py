from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from core.common.database import get_async_db_session
from core.utils.token import Token

oauth2_scheme = HTTPBearer()


async def authenticate_token(
        credential: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_async_db_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = credential.credentials
    service = Token(db)
    return await service.verify_access_token(token, credentials_exception)
