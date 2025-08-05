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


class DefaultRoleEnum(Enum):
    ADMIN = (1, "admin")
    DOCTOR = (2, "doctor")
    PATIENT = (3, "patient")

    def __new__(cls, id: int, name: str):
        obj = object.__new__(cls)
        obj.role_id = id
        obj.role_name = name
        return obj
