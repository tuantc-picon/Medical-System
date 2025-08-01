from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.common.database import get_async_db_session
from core.utils.token import Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class Authenticate:
    def authenticate_token(self, token_client: str = Depends(oauth2_scheme),
                           db: AsyncSession = Depends(get_async_db_session)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        token_use = Token(db)
        return token_use.verify_access_token(token_client, credentials_exception)
