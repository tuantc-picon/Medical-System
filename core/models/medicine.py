from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Date
from sqlalchemy.orm import relationship
from . import Base


class DrugAllergy(Base):
    __tablename__ = 'drug_allergy'
    id = Column(Integer, primary_key=True)
    # Forkey
    medicine_id = Column(Integer, ForeignKey('medicine.id'))
    patient_id = Column(Integer, ForeignKey('patient.id'))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # relationship
    patient = relationship("Patient", back_populates="drug_allergies")
    medicine = relationship("Medicine", back_populates="drug_allergies")


class Medicine(Base):
    __tablename__ = 'medicine'
    id = Column(Integer, primary_key=True)
    # Forkey
    medicine_batch_id = Column(Integer, ForeignKey('medicine_batch.id'))

    Medicine_name = Column(String,nullable=False)
    price_unit = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # relationship
    drug_allergies = relationship(DrugAllergy, back_populates="medicine")
    medicine_batch = relationship("MedicineBatch", back_populates="medicine")
    prescription_detail = relationship("PrescriptionDetail", back_populates="medicine")




class MedicineBatch(Base):
    __tablename__ = 'medicine_batch'
    id = Column(Integer, primary_key=True)
    unit_price = Column(Integer,nullable=False)
    current_quantity = Column(Integer,nullable=False)
    note = Column(String)
    expiry_date= Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # relationship
    medicine = relationship("Medicine", back_populates="medicine_batch")
    prescription_detail = relationship("PrescriptionDetail", back_populates="medicine_batch")



