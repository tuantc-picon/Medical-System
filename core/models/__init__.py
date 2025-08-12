from core.common.Base import BaseModel
from .appointement import Appointment, Hospitalization
from .certificate import DoctorCertificate, Certificate
from .invoice import InvoicePrescription, InvoiceMedical, InvoiceHospitalized
from .medicine import Medicine, MedicineBatch, DrugAllergy
from .prescription import Prescription, PrescriptionDetail
from .schedule import WorkSchedule, WorkScheduleDetail
from .token import ListToken
from .user import User, Admin, Doctor, Patient
from .role import Role, RolePermission, Permission
