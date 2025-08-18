from app.users.schemas.user import UserCreateSchema
from core.common.database import get_async_db_session
from api.common import handlers
from core import services
from .register import register as router_register
from .authentication import authentication as router_authentication
from .schedule import schedule as router_schedule
from .role import role as router_role
from .user import user_router as router_user

from fastapi import APIRouter

router_v1 = APIRouter(redirect_slashes=False, prefix="/v1")


router_v1.include_router(router_register)
router_v1.include_router(router_authentication)
router_v1.include_router(router_schedule)
router_v1.include_router(router_role)
router_v1.include_router(router_user)
