from fastapi import APIRouter
from api.v1.users import router as users_v1
router = APIRouter(redirect_slashes=False)


router.include_router(users_v1)


@router.get("/health")
def health_check():
    return {"status": "healthy"}
