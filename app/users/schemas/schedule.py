from core.schemas.base import MSBaseSchema
from typing import Optional
from datetime import datetime


class ScheduleDoctorCreate(MSBaseSchema):
    doctor_id: int
    start_time: datetime
    end_time: datetime
    note: Optional[str] = None
