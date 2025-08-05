from app.users.schemas import doctor, patient, admin
from core.common.Base import BaseService
from core.models.role import Role
from core.models.user import Doctor, Patient, Admin
from core.utils.hashing import Hash


class Register(BaseService):
    async def admin(self, user_data: admin.AdminCreate):
        role_admin = await self.fetch_one(Role, name="admin")
        new_admin = Admin(
            name=user_data.name,
            email=user_data.email,
            password=Hash.bcrypt(user_data.password),
            gender=user_data.gender,
            age=user_data.age,
            role_id=role_admin.id,
            phone_number=user_data.phone_number,
            address=user_data.address
        )
        await self._save(new_admin)
        return new_admin

    async def patient(self, user_data: patient.PatientCreate):
        role_patient = await self.fetch_one(Role, name="patient")
        new_patient = Patient(
            name=user_data.name,
            email=user_data.email,
            password=Hash.bcrypt(user_data.password),
            gender=user_data.gender,
            age=user_data.age,
            role_id=role_patient.id,
            job=user_data.job,
            insurance_number=user_data.insurance_number
        )
        await self._save(new_patient)
        return new_patient

    async def doctor(self, user_data: doctor.DoctorCreate):
        role_doctor = await self.fetch_one(Role, name="doctor")
        new_doctor = Doctor(
            name=user_data.name,
            email=user_data.email,
            password=Hash.bcrypt(user_data.password),
            gender=user_data.gender,
            age=user_data.age,
            role_id=role_doctor.id,
            specialization=user_data.specialization,
            graduated_at=user_data.graduated_at
        )
        await self._save(new_doctor)
        return new_doctor
