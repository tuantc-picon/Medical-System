from sqlalchemy.ext.asyncio import AsyncSession
from app.users.schemas.schedule import ScheduleDoctorCreate
from core.models import ScheduleDoctor


async def create_schedule(schedule: ScheduleDoctorCreate, db: AsyncSession):
    new_schedule = ScheduleDoctor(
        doctor_id=schedule.doctor_id,
        start_time=schedule.start_time,
        end_time=schedule.end_time,
        note=schedule.note
    )
    db.add(new_schedule)
    await db.commit()
    await db.refresh(new_schedule)
    return new_schedule