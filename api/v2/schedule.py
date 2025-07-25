from fastapi import APIRouter, Depends, status

from core.common.constants import RoleEnum
from core.services.schedule import create_schedule
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.schemas.schedule import ScheduleDoctorCreate
from core.common.database import get_async_db_session


schedule_router = APIRouter(
    prefix="/v2/schedule",
    tags=["Schedule"]
)

@schedule_router.post("/", status_code=status.HTTP_201_CREATED)
async def createSchedule(schedule: ScheduleDoctorCreate,
                         db:AsyncSession = Depends(get_async_db_session)):
    return await create_schedule(schedule, db)