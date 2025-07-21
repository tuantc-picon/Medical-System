from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import relationship

from . import StatusInvoiceEnum, Appointment
from core.common.Base import BaseModel

class InvoicePrescription(BaseModel):
    __tablename__ = 'invoice_prescription'
    # Forkey
    prescription_id = Column(Integer, ForeignKey('prescription.id'))

    status = Column(Enum(StatusInvoiceEnum), nullable=False)
    total_amount = Column(Integer, nullable=False)
    payment_time = Column(DateTime(timezone=True), nullable=True)
    # relationship
    prescription = relationship("Prescription", back_populates="invoice_Prescription")


class InvoiceMedical(BaseModel):
    __tablename__ = 'invoice_medical'
    # Forkey
    appointment_id = Column(Integer, ForeignKey('appointment.id'))

    total_amount = Column(Integer, nullable=False)
    payment_time = Column(DateTime(timezone=True), nullable=True)
    # relationship
    appointment = relationship(Appointment, back_populates="invoice_medical")


class InvoiceHospitalized(BaseModel):
    __tablename__ = 'invoice_hospitalized'
    # Forkey
    Hospitalized_id = Column(Integer, ForeignKey('hospitalization.id'))

    total_days = Column(Integer, nullable=False)
    total_amount = Column(Integer, nullable=False)
    payment_time = Column(DateTime(timezone=True), nullable=True)
    # relationship
    hospitalization = relationship("Hospitalization", back_populates="invoice_hospitalized")