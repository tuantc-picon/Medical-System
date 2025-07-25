from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from . import Base


class PrescriptionDetail(Base):
    __tablename__ = 'prescriptions_detail'

    id = Column(Integer, primary_key=True)
    # Foreign Keys
    prescription_id = Column(Integer, ForeignKey('prescription.id'))
    medicine_id = Column(Integer, ForeignKey('medicine.id'))
    batch_id = Column(Integer, ForeignKey('medicine_batch.id'))

    quantity = Column(Integer)
    expiry_medicine = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    prescription = relationship("Prescription", back_populates="prescription_detail")
    medicine = relationship("Medicine", back_populates="prescription_detail")
    medicine_batch = relationship("MedicineBatch", back_populates="prescription_detail")


class Prescription(Base):
    __tablename__ = 'prescription'

    id = Column(Integer, primary_key=True)
    appointment_id = Column(Integer, ForeignKey('appointment.id'))

    Dosage = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    appointments = relationship("Appointment", back_populates="prescription")
    prescription_detail = relationship("PrescriptionDetail", back_populates="prescription")
    invoice_Prescription = relationship("InvoicePrescription", back_populates="prescription")
