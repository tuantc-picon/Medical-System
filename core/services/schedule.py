from fastapi import HTTPException, status
from sqlalchemy import select

from app.users.schemas.schedule import (
    ScheduleDoctorCreateSchema,
    ScheduleDoctorBaseSchema,
)
from core.common.Base import BaseService
from core.models.schedule import ScheduleDoctor
from app.users.schemas.schedule import ScheduleDoctorCreateSchema


class Schedule(BaseService):
    async def verify_schedule(self, schedule: ScheduleDoctorCreateSchema):
        try:
            stmt = select(ScheduleDoctor).where(
                ScheduleDoctor.doctor_id == schedule.doctor_id,
                ScheduleDoctor.start_time < schedule.end_time,
                ScheduleDoctor.end_time > schedule.start_time,
            )
            result = await self.db.execute(stmt)
            schedule_doctor = result.scalar_one_or_none()

            if schedule_doctor:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Schedule conflict detected. Please choose a different time slot.",
                )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error while checking schedule.",
            )

        return True

    async def create_doctor_schedule(self, requires: ScheduleDoctorCreateSchema):
        await self.verify_schedule(requires)
        new_schedule = ScheduleDoctor(
            doctor_id=requires.doctor_id,
            start_time=requires.start_time,
            end_time=requires.end_time,
            note=requires.note,
        )

        await self._save(new_schedule)
        return ScheduleDoctorBaseSchema.model_validate(new_schedule)
