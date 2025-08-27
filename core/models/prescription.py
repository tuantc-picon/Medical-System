from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from core.common.Base import BaseModel


class PrescriptionDetail(BaseModel):
    __tablename__ = 'prescriptions_detail'
    # Foreign Keys
    prescription_id = Column(Integer, ForeignKey('prescription.id'))
    medicine_id = Column(Integer, ForeignKey('medicine.id'))

    quantity = Column(Integer)
    expiry_medicine = Column(DateTime(timezone=True))
    # Relationships
    prescription = relationship("Prescription", back_populates="prescription_details")
    medicine = relationship("Medicine", back_populates="prescription_details")


class Prescription(BaseModel):
    __tablename__ = 'prescription'

    appointment_id = Column(Integer, ForeignKey('appointment.id'), unique=True)

    dosage = Column(String)
    # Relationships
    appointment = relationship("Appointment", back_populates="prescription")
    prescription_details = relationship("PrescriptionDetail", back_populates="prescription")
    invoice_prescription = relationship("InvoicePrescription", back_populates="prescription", uselist=False)
