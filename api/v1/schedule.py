from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.schemas.schedule import ScheduleDoctorCreate
from core.common.database import get_async_db_session
from core.services.oauth2 import bearer_scheme
from core.services.schedule import Schedule as ScheduleService

schedule = APIRouter(
    prefix="/v2/schedule",
    tags=["Schedule"]
)


@schedule.post("/create", status_code=status.HTTP_201_CREATED)
async def create_schedule_doctor(requires: ScheduleDoctorCreate,
                                 a=Depends(bearer_scheme),
                                 db: AsyncSession = Depends(get_async_db_session)):
    use = ScheduleService(db)
    return await use.doctor_for_the_day(requires)
