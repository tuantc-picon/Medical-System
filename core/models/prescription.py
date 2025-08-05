from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from core.common.Base import BaseModel


class PrescriptionDetail(BaseModel):
    __tablename__ = 'prescriptions_detail'
    # Foreign Keys
    prescription_id = Column(Integer, ForeignKey('prescription.id'))
    medicine_id = Column(Integer, ForeignKey('medicine.id'))
    batch_id = Column(Integer, ForeignKey('medicine_batch.id'))

    quantity = Column(Integer)
    expiry_medicine = Column(DateTime(timezone=True))
    # Relationships
    prescription = relationship("Prescription", back_populates="prescription_detail")
    medicine = relationship("Medicine", back_populates="prescription_detail")
    medicine_batch = relationship("MedicineBatch", back_populates="prescription_detail")


class Prescription(BaseModel):
    __tablename__ = 'prescription'

    appointment_id = Column(Integer, ForeignKey('appointment.id'))

    Dosage = Column(String)
    # Relationships
    appointments = relationship("Appointment", back_populates="prescription")
    prescription_detail = relationship("PrescriptionDetail", back_populates="prescription")
    invoice_Prescription = relationship("InvoicePrescription", back_populates="prescription")
