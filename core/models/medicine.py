from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from core.common.Base import BaseModel


class DrugAllergy(BaseModel):
    __tablename__ = 'drug_allergy'
    # Forkey
    medicine_id = Column(Integer, ForeignKey('medicine.id'))
    patient_id = Column(Integer, ForeignKey('patient.id'))
    # relationship
    patient = relationship("Patient", back_populates="drug_allergies")
    medicine = relationship("Medicine", back_populates="drug_allergies")


class Medicine(BaseModel):
    __tablename__ = 'medicine'

    Medicine_name = Column(String, nullable=False)
    price_unit = Column(Integer, nullable=False)
    unit = Column(String, nullable=False)

    # Relationships
    drug_allergies = relationship("DrugAllergy", back_populates="medicine")
    medicine_batch = relationship("MedicineBatch", back_populates="medicine")
    prescription_details = relationship("PrescriptionDetail", back_populates="medicine")


class MedicineBatch(BaseModel):
    __tablename__ = 'medicine_batch'

    medicine_id = Column(Integer, ForeignKey('medicine.id'), nullable=False)
    unit_price = Column(Integer, nullable=False)
    current_quantity = Column(Integer, nullable=False)
    initial_quantity = Column(Integer, nullable=False)
    note = Column(String)
    expiry_date = Column(Date, nullable=False)

    # Relationships
    medicine = relationship("Medicine", back_populates="medicine_batch")
