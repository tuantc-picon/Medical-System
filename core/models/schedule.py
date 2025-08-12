from sqlalchemy import Integer, String, DateTime, Column, ForeignKey
from sqlalchemy.orm import relationship

from core.common.Base import BaseModel


class WorkSchedule(BaseModel):
    __tablename__ = 'work_schedule'
    doctor_id = Column(Integer, ForeignKey('doctor.id'))
    schedule_detail_id = Column(Integer, ForeignKey('work_schedule_detail.id'))
    doctor = relationship("Doctor", back_populates="schedules")
    work_schedule_details = relationship("WorkScheduleDetail", back_populates="work_schedule")


class WorkScheduleDetail(BaseModel):
    __tablename__ = 'work_schedule_detail'
    # Forkey
    __table_args__ = {'extend_existing': True}

    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    note = Column(String)
    # relationship
    work_schedule = relationship("WorkSchedule", back_populates="work_schedule_details")
