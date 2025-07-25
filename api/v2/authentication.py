from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from core.common.database import get_async_db_session
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
from core.services.authention import login as LOGIN

Login = APIRouter(
    prefix="/v2/login",
    tags=["authentication"]
)


@Login.post("/")
async def login(    request: OAuth2PasswordRequestForm = Depends(),
                    db:AsyncSession = Depends(get_async_db_session) ):
    return await LOGIN(request, db)