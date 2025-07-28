from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from core.common.Base import BaseModel


class DoctorCertificate(BaseModel):
    __tablename__ = 'doctor_certificate'
    # Forkey
    doctor_id = Column(Integer, ForeignKey('doctor.id'))
    certificate_id = Column(Integer, ForeignKey('certificate.id'))
    # realtionship
    doctor = relationship("Doctor", back_populates="doctor_certificates")
    certificate = relationship("Certificate", back_populates="doctor_certificates")



class Certificate(BaseModel):
    __tablename__ = 'certificate'
    archived_id = Column(DateTime(timezone=True), nullable=False)
    # relationship
    doctor_certificates = relationship("DoctorCertificate", back_populates="certificate")