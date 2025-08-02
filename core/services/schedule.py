from fastapi import HTTPException, status
from sqlalchemy import select

from app.users.schemas.schedule import ScheduleDoctorCreate
from core.common.Base import BaseService
from core.models.schedule import ScheduleDoctor


class Schedule(BaseService):
    async def verify_schedule(self, schedule: ScheduleDoctorCreate):
        if schedule.start_time >= schedule.end_time:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Time slot cannot be greater than time slot.")
        try:
            stmt = select(ScheduleDoctor).where(
                ScheduleDoctor.doctor_id == schedule.doctor_id,
                ScheduleDoctor.end_time <= schedule.start_time,
                ScheduleDoctor.start_time >= schedule.end_time)
            result = await self.db.execute(stmt)
            schedule_doctor = result.scalar_one_or_none()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error checking schedule: {str(e)}"
            )
        if schedule_doctor:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Schedule conflict detected. Please choose a different time slot.")
        return True

    async def doctor_for_the_day(self, requires: ScheduleDoctorCreate):
        await self.verify_schedule(requires)
        new_schedule = ScheduleDoctor(
            doctor_id=requires.doctor_id,
            start_time=requires.start_time,
            end_time=requires.end_time,
            note=requires.note
        )
        await self._save(new_schedule)
        return new_schedule
