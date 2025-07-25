from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from core.common.database import get_async_db_session
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
from core.services.authention import login as LOGIN
from core.services.role_base import require_role

Login = APIRouter(
    tags=["authentication"]
)


@Login.post("/login")
async def login(db:AsyncSession = Depends(get_async_db_session),

                request: OAuth2PasswordRequestForm = Depends()):
    return await LOGIN(db, request)