from fastapi import APIRouter

router = APIRouter(redirect_slashes=False)

from api.v1.users import router as users_v1
from api.v1.authentication import authentication as authentication_v1
from api.v1.schedule import schedule as schedule_v1
from api.v1.role import role as role_v1

router.include_router(users_v1)
router.include_router(authentication_v1)
router.include_router(schedule_v1)
router.include_router(role_v1)


@router.get("/health")
def health_check():
    return {"status": "healthy"}
