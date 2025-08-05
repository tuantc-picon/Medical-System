from datetime import datetime
from typing import Optional

from pydantic import model_validator

from core.schemas.base import MSBaseSchema

class ScheduleDoctorBaseSchema(MSBaseSchema):
    doctor_id: int
    start_time: datetime
    end_time: datetime
    note: Optional[str] = None

class ScheduleDoctorCreateSchema(ScheduleDoctorBaseSchema):
    @model_validator(mode="before")
    def validate_time(cls, values: dict):
        start = values.get('start_time')
        end = values.get('end_time')
        if start and end and start >= end:
            raise ValueError("Start time must be earlier than end time.")
        return values

