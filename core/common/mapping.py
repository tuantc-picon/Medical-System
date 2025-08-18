from core.common.constants import DefaultRoleEnum
from app.users.schemas.admin import AdminReadSchema
from app.users.schemas.doctor import DoctorReadSchema
from app.users.schemas.patient import PatientReadSchema

ROLE_MAPPING_READ_SCHEMA = {
    DefaultRoleEnum.ADMIN.role_id: AdminReadSchema,
    DefaultRoleEnum.DOCTOR.role_id: DoctorReadSchema,
    DefaultRoleEnum.PATIENT.role_id: PatientReadSchema,
}
