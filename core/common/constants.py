from enum import Enum

PASSWORD_REGEX = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"


class SortType(int, Enum):
    NONE = 0
    DESC = 1
    ASC = -1


class StatusAppointmentEnum(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class GenderEnum(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class StatusInvoiceEnum(Enum):
    UNFINISHED = "unfinished"
    COMPLETED = "completed"


class Role(str, Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    PATIENT = "patient"


ROLE_HIERARCHY = {
    Role.ADMIN: 3,
    Role.DOCTOR: 2,
    Role.PATIENT: 1
}
