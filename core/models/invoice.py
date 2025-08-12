from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

from core.common.Base import BaseModelInvoice
from core.common.constants import StatusInvoiceEnum
from . import Appointment


class InvoicePrescription(BaseModelInvoice):
    __tablename__ = 'invoice_prescription'
    # Forkey
    prescription_id = Column(Integer, ForeignKey('prescription.id'), unique=True)

    status = Column(Enum(StatusInvoiceEnum), nullable=False)
    # relationship
    prescription = relationship("Prescription", back_populates="invoice_prescription", uselist=False)


class InvoiceMedical(BaseModelInvoice):
    __tablename__ = 'invoice_medical'
    # Forkey
    appointment_id = Column(Integer, ForeignKey('appointment.id'))

    # relationship
    appointment = relationship(Appointment, back_populates="invoice_medical", uselist=False)


class InvoiceHospitalized(BaseModelInvoice):
    __tablename__ = 'invoice_hospitalized'
    # Forkey
    hospitalized_id = Column(Integer, ForeignKey('hospitalization.id'))

    total_days = Column(Integer, nullable=False)
    # relationship
    hospitalization = relationship("Hospitalization", back_populates="invoice_hospitalized")
