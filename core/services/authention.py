from datetime import datetime, timezone

from fastapi import HTTPException, status
from jose import JWTError

from app.users.schemas.user import UserLoginSchema
from core.common.Base import BaseService
from core.models.token import ListToken
from core.models.user import User
from core.utils.hashing import Hash
from core.services.token import TokenService


class AuthentionService(BaseService):
    async def _generate_tokens(self, query_user: User):
        try:
            access_token = TokenService.create_access_token(
                data={
                    "subEmail": query_user.email,
                    "subName": query_user.name,
                    "role_id": query_user.role_id,
                }
            )
            refresh_token = TokenService.create_refresh_token(
                data={"subID": query_user.id, "subEmail": query_user.email}
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Token encoding failed.",
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Token generation failed.",
            )
        new_token = ListToken(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=query_user.id,
        )
        await self._save(new_token)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
        }  # returned in API response body => oauth2 standard

    async def login_user(self, request: UserLoginSchema):
        query_user = await self.fetch_one(User, email=request.email)
        if not query_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not Hash.verify(request.password, query_user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        return await self._generate_tokens(query_user)

    async def logout_user(self, access_token: str):
        token = await self.fetch_one(ListToken, access_token=access_token)
        if not token or token.deleted_at:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Access token not found in online list.",
            )
        token.deleted_at = datetime.now(timezone.utc)
        await self._save(token)
        return {"message": "Logout successful."}

    async def renew_token(self, refresh_access_token: str):
        token_service = TokenService(db=self.db)
        user_data = await token_service.verify_refresh_token(refresh_access_token)
        query = await self.fetch_one(
            ListToken, refresh_token=refresh_access_token, deleted_at=None
        )

        await self.logout_user(query.access_token)
        return await self._generate_tokens(user_data)
