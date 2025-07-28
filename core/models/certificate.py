from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from . import Base


class DoctorCertificate(Base):
    __tablename__ = 'doctor_certificate'
    # Forkey
    doctor_id = Column(Integer, ForeignKey('doctor.id'))
    certificate_id = Column(Integer, ForeignKey('certificate.id'))
    archived_dateTime = Column(DateTime(timezone=True), nullable=False)
    # realtionship
    doctor = relationship("Doctor", back_populates="doctor_certificates")
    certificate = relationship("Certificate", back_populates="doctor_certificates")



class Certificate(Base):
    __tablename__ = 'certificate'
    certificate_name = Column(String, nullable=False)
    certificate_code = Column(String, nullable=False, unique=True)
    # relationship
    doctor_certificates = relationship("DoctorCertificate", back_populates="certificate")