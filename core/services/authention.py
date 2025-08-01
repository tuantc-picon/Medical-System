from datetime import datetime, timezone

from fastapi import HTTPException, status
from jose import JWTError

from app.users.schemas.user import UserLogin
from core.common.Base import BaseService
from core.models.token import ListToken
from core.models.user import User
from core.utils.hashing import Hash
from core.utils.token import Token


class AuthentionService(BaseService):
    async def _generate_tokens(self, query_user: User):
        try:
            access_token = Token.create_access_token(data={
                "subEmail": query_user.email,
                "subName": query_user.name,
                "role": query_user.role.value})
            refresh_token = Token.create_refresh_token(data={
                "subID": query_user.id,
                "subEmail": query_user.email
            })
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Token encoding failed."
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Token generation failed."
            )
        new_online = ListToken(access_token=access_token,
                               refresh_token=refresh_token,
                               user_id=query_user.id)
        await self._save(new_online)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "role": query_user.role.value,
            "token_type": "Bearer"
        }

    async def login(self, request: UserLogin):
        query_user = await self.fetch_one(User, email=request.email)
        if not query_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not Hash.verify(request.password, query_user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
        return await self._generate_tokens(query_user)

    async def logout(self, tokenAccess: str, tokenRefresh: str):
        online_token = await self.fetch_one(ListToken, access_token=tokenAccess, refresh_token=tokenRefresh)
        if not online_token or online_token.deleted_at:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Access token not found in online list."
            )
        online_token.deleted_at = datetime.now(timezone.utc)
        await self._save(online_token)
        return {
            "message": "Logout successful."
        }

    async def refresh_token(self, refresh_access_token: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        test = Token(db=self.db)
        user_data = await test.verify_refresh_token(refresh_access_token, credentials_exception)
        query = await self.fetch_one(ListToken,
                                     refresh_token=refresh_access_token,
                                     deleted_at=None)

        await self.logout(query.access_token, refresh_access_token)
        return await self._generate_tokens(user_data)
