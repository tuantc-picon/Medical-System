from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.services import query
from core.utils.token import create_access_token, create_refresh_token

async def login( request: OAuth2PasswordRequestForm, db : AsyncSession):
    query_user=await query.verify_authention(request.username, request.password, db)
    if not query_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"subEmail": query_user.email,
                                             "subName": query_user.name,
                                             "role": query_user.role.value})
    refresh_token = create_refresh_token(data={"sub": query_user.email})
    return {"access_token": access_token,
            "refresh_token": refresh_token,
            "role": query_user.role,
            "token_type": "Bearer"
            }