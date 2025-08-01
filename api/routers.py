from fastapi import APIRouter

router = APIRouter(redirect_slashes=False)

from api.v1.users import router as users_v1
from api.v1.authentication import Login as login_v1

router.include_router(users_v1)
router.include_router(login_v1)


@router.get("/health")
def health_check():
    return {"status": "healthy"}
