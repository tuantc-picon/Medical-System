from app.users.schemas.admin import AdminCreateSchema
from app.users.schemas.doctor import DoctorCreateSchema
from app.users.schemas.patient import PatientCreateSchema
from app.users.schemas.user import UserResponseSchema
from core.common.Base import BaseService
from core.models.user import Doctor, Patient, Admin
from core.utils.hashing import Hash

from typing import Type, Any


class RegisterService(BaseService):
    async def _register_user(
        self,
        user_model: Type[Any],
        schema_data,
        extra_fields: dict = None,
    ):
        base_fields = {
            "name": schema_data.name,
            "email": schema_data.email,
            "password": Hash.bcrypt(schema_data.password),
            "gender": schema_data.gender,
            "age": schema_data.age,
            "role_id": schema_data.role_id,
        }

        if extra_fields:
            base_fields.update(extra_fields)

        user = await self._save(user_model(**base_fields))
        user.extra_fields = extra_fields
        user_data = UserResponseSchema.model_validate(user)
        return user_data

    async def register_admin(self, user_data: AdminCreateSchema):
        extra = {
            "phone_number": user_data.extra_fields.get("phone_number"),
            "address": user_data.extra_fields.get("address"),
        }
        return await self._register_user(Admin, user_data, extra)

    async def register_doctor(
        self,
        user_data: DoctorCreateSchema,
    ):
        extra = {
            "specialization": user_data.extra_fields.get("specialization"),
            "graduated_at": user_data.extra_fields.get("graduated_at"),
        }
        return await self._register_user(Doctor, user_data, extra)

    async def register_patient(self, user_data: PatientCreateSchema):
        extra = {
            "job": user_data.extra_fields.get("job"),
            "insurance_number": user_data.extra_fields.get("insurance_number"),
        }
        return await self._register_user(Patient, user_data, extra)
