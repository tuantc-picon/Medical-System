import enum
from sqlalchemy import Integer, String, DateTime, Column, ForeignKey, func, Enum
from sqlalchemy.orm import relationship
from . import Base, StatusAppointmentEnum


class Appointment(Base):
    __tablename__ = 'appointment'
    id = Column(Integer, primary_key=True)
    # Forkey
    patient_id = Column(Integer, ForeignKey('patient.id'))
    doctor_id = Column(Integer,ForeignKey('doctor.id'))

    status = Column(Enum(StatusAppointmentEnum), nullable=False)
    cancel_reason = Column(String, nullable=False)
    diagnosis = Column(String)
    medical_notes = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # relationship Appointment
    doctor = relationship("Doctor", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")
    prescription = relationship("Prescription", back_populates="appointments")
    hospitalization = relationship("Hospitalization", back_populates="appointment")
    invoice_medical = relationship("InvoiceMedical", back_populates="appointment")


class ScheduleDoctor(Base):
    __tablename__ = 'schedule_doctor'
    id = Column(Integer, primary_key=True)
    # Forkey
    doctor_id = Column(Integer, ForeignKey('doctor.id'))

    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    note = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    #relationship
    doctor = relationship("Doctor", back_populates="schedules")



class Hospitalization(Base):
    __tablename__ = 'hospitalization'
    id = Column(Integer, primary_key=True)
    # Forkey
    appointment_id = Column(Integer, ForeignKey('appointment.id'), unique=True)

    room_number = Column(Integer, nullable=False)
    bed_number = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # relationship
    appointment = relationship(Appointment, back_populates="hospitalization", uselist=False)
    invoice_hospitalized = relationship("InvoiceHospitalized", back_populates="hospitalization")

