from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.schemas.schedule import ScheduleDoctorCreate
from core.common.database import get_async_db_session
from core.services.schedule import Schedule as ScheduleService
from core.utils.authorize import authorize_user

schedule = APIRouter(
    prefix="/v1/schedule",
    tags=["Schedule"]
)


@schedule.post("/create", status_code=status.HTTP_201_CREATED)
async def create_schedule_doctor(requires: ScheduleDoctorCreate,
                                 authorize=Depends(authorize_user),
                                 db: AsyncSession = Depends(get_async_db_session)):
    use = ScheduleService(db)
    return await use.create_doctor_schedule(requires)

# _=Depends(authorize_user)
