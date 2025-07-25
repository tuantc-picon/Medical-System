from sqlalchemy import Integer, String, DateTime, Column, ForeignKey
from sqlalchemy.orm import relationship

from core.common.Base import BaseModel


class ScheduleDoctor(BaseModel):
    __tablename__ = 'schedule_doctor'
    # Forkey
    doctor_id = Column(Integer, ForeignKey('doctor.id'))

    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    note = Column(String)
    # relationship
    doctor = relationship("Doctor", back_populates="schedules")
