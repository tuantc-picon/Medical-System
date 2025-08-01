from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from ..common.Base import BaseModel


class DoctorCertificate(BaseModel):
    __tablename__ = 'doctor_certificate'
    # Forkey
    doctor_id = Column(Integer, ForeignKey('doctor.id'))

    certificate_id = Column(Integer, ForeignKey('certificate.id'))
    archived_dateTime = Column(DateTime(timezone=True), nullable=False)
    # realtionship
    doctor = relationship("Doctor", back_populates="doctor_certificates")
    certificate = relationship("Certificate", back_populates="doctor_certificates")


class Certificate(BaseModel):
    __tablename__ = 'certificate'
    certificate_name = Column(String, nullable=False)
    certificate_code = Column(String, nullable=False, unique=True)
    # relationship
    doctor_certificates = relationship("DoctorCertificate", back_populates="certificate")
