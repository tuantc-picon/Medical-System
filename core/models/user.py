from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from core.common.Base import BaseModel
from core.common.constants import GenderEnum, DefaultRoleEnum


class User(BaseModel):
    __tablename__ = 'users'
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)

    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    age = Column(Integer)

    __mapper_args__ = {
        'polymorphic_on': role_id,  # identification column -> which column to use to identify.
        'with_polymorphic': '*'
        # load full subclass information when querying User => can query element subclass when query Baseclass
    }
    list_tokens = relationship("ListToken", back_populates="user", lazy="selectin")
    role = relationship("Role", back_populates="users")


class Admin(User):
    __tablename__ = 'admin'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    phone_number = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': DefaultRoleEnum.ADMIN.role_id
    }


class Doctor(User):
    __tablename__ = 'doctor'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    specialization = Column(String, nullable=False)
    graduated_at = Column(String, nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': DefaultRoleEnum.DOCTOR.role_id
    }
    # relationship Doctor
    appointments = relationship("Appointment", back_populates="doctor")
    schedules = relationship("WorkSchedule", back_populates="doctor")
    doctor_certificates = relationship("DoctorCertificate", back_populates="doctor")


class Patient(User):
    __tablename__ = 'patient'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    job = Column(String)
    insurance_number = Column(String)
    __mapper_args__ = {
        'polymorphic_identity': DefaultRoleEnum.PATIENT.role_id
    }
    # relation Patient
    appointments = relationship("Appointment", back_populates="patient")
    drug_allergies = relationship("DrugAllergy", back_populates="patient")
