from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Enum, func
from . import Base, RoleEnum, GenderEnum # đã định nghĩa trong __init__.py
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String,nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    age = Column(Integer)
    role = Column(Enum(RoleEnum), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __mapper_args__ = {
        'polymorphic_on': role, # cột định danh -> lấy cột nào để xác định.
        'polymorphic_identity': 'user' # cột nhận diện -> admin, doctor, patient
    }


class Admin(User):
    __tablename__ = 'admin'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    phone_number = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': RoleEnum.ADMIN.value
    }

class Doctor(User):
    __tablename__ = 'doctor'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    specialization = Column(String, nullable=False)
    graduated_at = Column(String, nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': RoleEnum.DOCTOR.value
    }
    # relationship Doctor
    appointments = relationship("Appointment", back_populates="doctor")
    schedules = relationship("ScheduleDoctor", back_populates="doctor")
    doctor_certificates = relationship("DoctorCertificate", back_populates="doctor")



class Patient(User):
    __tablename__ = 'patient'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    job = Column(String)
    insurance_number = Column(String)
    __mapper_args__ = {
        'polymorphic_identity': RoleEnum.PATIENT.value
    }
    # relation Patient
    appointments = relationship("Appointment", back_populates="patient")
    drug_allergies = relationship("DrugAllergy", back_populates="patient")
