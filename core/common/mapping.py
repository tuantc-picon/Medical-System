from app.users.schemas.admin import AdminCreateSchema
from app.users.schemas.doctor import DoctorCreateSchema
from app.users.schemas.patient import PatientCreateSchema
from core.common.constants import DefaultRoleEnum
from app.users.schemas.admin import AdminReadSchema
from app.users.schemas.doctor import DoctorReadSchema
from app.users.schemas.patient import PatientReadSchema

ROLE_MAPPING_READ = {
    DefaultRoleEnum.ADMIN.role_id: AdminReadSchema,
    DefaultRoleEnum.DOCTOR.role_id: DoctorReadSchema,
    DefaultRoleEnum.PATIENT.role_id: PatientReadSchema,
}

ROLE_MAPPING_CREATE = {
    DefaultRoleEnum.ADMIN.role_id: (AdminCreateSchema, "register_admin"),
    DefaultRoleEnum.DOCTOR.role_id: (DoctorCreateSchema, "register_doctor"),
    DefaultRoleEnum.PATIENT.role_id: (PatientCreateSchema, "register_patient"),
}
