from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.schemas.schedule import ScheduleDoctorCreate
from core.common.database import get_async_db_session
from core.services.schedule import Schedule as ScheduleService
from core.utils.authorize import authorize_user

schedule = APIRouter(prefix="/v1/schedule", tags=["Schedule"])


@schedule.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_schedule_doctor(
    schedule_doctor: ScheduleDoctorCreate,
    authorized_user: bool = Depends(authorize_user("schedule:get")),
    db: AsyncSession = Depends(get_async_db_session),
):
    service = ScheduleService(db)
    return await service.create_doctor_schedule(schedule_doctor)
