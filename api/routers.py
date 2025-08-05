from fastapi import APIRouter

router = APIRouter(redirect_slashes=False)

from api.v1 import router_v1

router.include_router(router_v1)


@router.get("/health")
def health_check():
    return {"status": "healthy"}
