from fastapi import HTTPException
from app.users.schemas.user import UserResponseSchema
from core.common.Base import BaseService
from core.models.user import Doctor, Patient, Admin
from core.utils.hashing import Hash
from core.common.constants import DefaultRoleEnum
from app.users.schemas.user import UserCreateSchema

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

    async def register_user_information(self, user_data: UserCreateSchema):
        extra = {
            "phone_number": user_data.extra_fields.get("phone_number"),
            "address": user_data.extra_fields.get("address"),
            "specialization": user_data.extra_fields.get("specialization"),
            "graduated_at": user_data.extra_fields.get("graduated_at"),
            "job": user_data.extra_fields.get("job"),
            "insurance_number": user_data.extra_fields.get("insurance_number"),
        }
        if user_data.role_id == DefaultRoleEnum.ADMIN.role_id:
            model = Admin
        elif user_data.role_id == DefaultRoleEnum.DOCTOR.role_id:
            model = Doctor
        elif user_data.role_id == DefaultRoleEnum.PATIENT.role_id:
            model = Patient
        else:
            raise HTTPException(status_code=400, detail="Incorrect user input")

        model_fields = {c.name for c in model.__table__.columns}
        filtered_extra = {k: v for k, v in extra.items() if k in model_fields and v is not None}
        return await self._register_user(model, user_data, filtered_extra)
