from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from . import RoleEnum, GenderEnum
from sqlalchemy.orm import relationship

from core.common.Base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String,nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    age = Column(Integer)
    role = Column(Enum(RoleEnum), nullable=False)

    __mapper_args__ = {
        'polymorphic_on': role, # cột định danh -> lấy cột nào để xác định.
        'polymorphic_identity': RoleEnum # cột nhận diện -> admin, doctor, patient
    }
    list_tokens = relationship("ListToken", back_populates="user", lazy="selectin")


class Admin(User):
    __tablename__ = 'admin'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    phone_number = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': RoleEnum.ADMIN
    }



class Doctor(User):
    __tablename__ = 'doctor'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    specialization = Column(String, nullable=False)
    graduated_at = Column(String, nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': RoleEnum.DOCTOR
    }
    # relationship Doctor
    appointments = relationship("Appointment", back_populates="doctor")
    schedules = relationship("ScheduleDoctor", back_populates="doctor")
    doctor_certificates = relationship("DoctorCertificate", back_populates="doctor" )



class Patient(User):
    __tablename__ = 'patient'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    job = Column(String)
    insurance_number = Column(String)
    __mapper_args__ = {
        'polymorphic_identity': RoleEnum.PATIENT
    }
    # relation Patient
    appointments = relationship("Appointment", back_populates="patient")
    drug_allergies = relationship("DrugAllergy", back_populates="patient")
