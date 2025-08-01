from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils.token import Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


async def authenticate_token(db: AsyncSession, token_client: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    use = Token(db)
    await use.verify_access_token(token_client, credentials_exception)
