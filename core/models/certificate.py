from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from . import Base


class DoctorCertificate(Base):
    __tablename__ = 'doctor_certificate'
    id = Column(Integer, primary_key=True)
    # Forkey
    doctor_id = Column(Integer, ForeignKey('doctor.id'))
    certificate_id = Column(Integer, ForeignKey('certificate.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # realtionship
    doctor = relationship("Doctor", back_populates="doctor_certificates")
    certificate = relationship("Certificate", back_populates="doctor_certificates")



class Certificate(Base):
    __tablename__ = 'certificate'
    id = Column(Integer, primary_key=True)
    archived_id = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # relationship
    doctor_certificates = relationship("DoctorCertificate", back_populates="certificate")