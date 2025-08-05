from sqlalchemy import Integer, String, Column, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship

from core.common.Base import BaseModel
from core.common.constants import StatusAppointmentEnum


class Appointment(BaseModel):
    __tablename__ = 'appointment'
    # Forkey
    patient_id = Column(Integer, ForeignKey('patient.id'))
    doctor_id = Column(Integer, ForeignKey('doctor.id'))

    status = Column(Enum(StatusAppointmentEnum), nullable=False)
    cancel_reason = Column(String)
    diagnosis = Column(String)
    medical_notes = Column(String)
    # relationship Appointment
    doctor = relationship("Doctor", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")
    prescription = relationship("Prescription", back_populates="appointments")
    hospitalization = relationship("Hospitalization", back_populates="appointment")
    invoice_medical = relationship("InvoiceMedical", back_populates="appointment")

class ScheduleDoctor(BaseModel):
    __tablename__ = 'schedule_doctor'
    # Forkey
    doctor_id = Column(Integer, ForeignKey('doctor.id'))

    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    note = Column(String)
    # relationship
    doctor = relationship("Doctor", back_populates="schedules")



class Hospitalization(BaseModel):
    __tablename__ = 'hospitalization'
    # Forkey
    appointment_id = Column(Integer, ForeignKey('appointment.id'), unique=True)

    room_number = Column(Integer, nullable=False)
    bed_number = Column(Integer, nullable=False)
    # relationship
    appointment = relationship(Appointment, back_populates="hospitalization", uselist=False)
    invoice_hospitalized = relationship("InvoiceHospitalized", back_populates="hospitalization")
