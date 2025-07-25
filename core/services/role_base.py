from fastapi import Depends, HTTPException, status
from .oauth2 import authenticate_token
from core.common.constants import RoleEnum
from app.users.schemas.token import TokenData


def require_role(required_roles: list[RoleEnum]):
    async def role_checker(
        current_user: TokenData = Depends(authenticate_token)
    ):
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action"
            )
        return current_user
    return role_checker
