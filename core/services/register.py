from app.users.schemas import user, doctor, patient, admin
from sqlalchemy.ext.asyncio import AsyncSession

from core.common.constants import RoleEnum, GenderEnum
from core.models.user import User, Doctor, Patient, Admin
from core.utils.hashing import Hash
from fastapi.encoders import jsonable_encoder


hash_password = Hash.bcrypt

async def register_admin(user_data: admin.AdminCreate, db: AsyncSession):
    new_admin = Admin(
        name=user_data.name,
        email=user_data.email,
        password=hash_password(user_data.password),
        gender=user_data.gender,
        age=user_data.age,
        role=RoleEnum.ADMIN,
        phone_number=user_data.phone_number,
        address=user_data.address
    )

    db.add(new_admin)
    await db.commit()
    await db.refresh(new_admin)
    return new_admin


async def register_patient(user_data: patient.PatientCreate, db: AsyncSession):
    new_patient = Patient(
        name=user_data.name,
        email=user_data.email,
        password=hash_password(user_data.password),
        gender=user_data.gender,
        age=user_data.age,
        role=RoleEnum.PATIENT,
        job=user_data.job,
        insurance_number=user_data.insurance_number
    )

    db.add(new_patient)
    await db.commit()
    await db.refresh(new_patient)
    return new_patient



async def register_doctor(user_data: doctor.DoctorCreate, db: AsyncSession):
    new_doctor = Doctor(
        name=user_data.name,
        email=user_data.email,
        password=hash_password(user_data.password),
        gender=user_data.gender,
        age=user_data.age,
        role=RoleEnum.DOCTOR,
        specialization=user_data.specialization,
        graduated_at=user_data.graduated_at
    )

    db.add(new_doctor)
    await db.commit()
    await db.refresh(new_doctor)
    return new_doctor

