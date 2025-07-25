from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils.token import Token

bearer_scheme = HTTPBearer()


async def authenticate_token(db: AsyncSession, credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_client = credentials.credentials
    use = Token(db)
    return await use.verify_access_token(token_client, credentials_exception)
