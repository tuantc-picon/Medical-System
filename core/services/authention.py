from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.services import query
from core.utils.token import create_access_token, create_refresh_token

async def login(db : AsyncSession, request: OAuth2PasswordRequestForm = Depends()):
    if not query.verify_authention(request.username, request.password, db):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": request.username})
    refresh_token = create_refresh_token(data={"sub": request.username})
    return {"access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
            }