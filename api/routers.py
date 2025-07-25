from fastapi import APIRouter
# from api.v1.users import router as users_v1


router = APIRouter(redirect_slashes=False)

# router.include_router(users_v1, prefix="/v1", tags=["Users"])
#
#
#
#
# @router.get("/health")
# def health_check():
#     return {"status": "healthy"}



from api.v2.users import router as users_v2
from api.v2.authentication import Login as login_v2

router.include_router(users_v2)
router.include_router(login_v2)




@router.get("/health")
def health_check():
    return {"status": "healthy"}
