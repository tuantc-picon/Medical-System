from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import relationship

from . import Base, StatusInvoiceEnum, Appointment


class InvoicePrescription(Base):
    __tablename__ = 'invoice_prescription'
    id = Column(Integer, primary_key=True)
    # Forkey
    prescription_id = Column(Integer, ForeignKey('prescription.id'))

    status = Column(Enum(StatusInvoiceEnum), nullable=False)
    total_amount = Column(Integer, nullable=False)
    payment_time = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # relationship
    prescription = relationship("Prescription", back_populates="invoice_Prescription")


class InvoiceMedical(Base):
    __tablename__ = 'invoice_medical'
    id = Column(Integer, primary_key=True)
    # Forkey
    appointment_id = Column(Integer, ForeignKey('appointment.id'))

    total_amount = Column(Integer, nullable=False)
    payment_time = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # relationship
    appointment = relationship(Appointment, back_populates="invoice_medical")


class InvoiceHospitalized(Base):
    __tablename__ = 'invoice_hospitalized'
    id = Column(Integer, primary_key=True)
    # Forkey
    Hospitalized_id = Column(Integer, ForeignKey('hospitalization.id'))

    total_days = Column(Integer, nullable=False)
    total_amount = Column(Integer, nullable=False)
    payment_time = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # relationship
    hospitalization = relationship("Hospitalization", back_populates="invoice_hospitalized")