from enum import Enum


PASSWORD_REGEX = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"


class SortType(int, Enum):
    NONE = 0
    DESC = 1
    ASC = -1


class StatusAppointmentEnum(Enum):
    PENDING = (1, "pending")
    CONFIRMED = (2, "confirmed")
    COMPLETED = (3, "completed")
    CANCELLED = (4, "cancelled")

    def __new__(cls, id: int, name: str):
        obj = object.__new__(cls)
        obj.status_id = id
        obj.status_name = name
        return obj


class GenderEnum(Enum):
    MALE = (1, "male")
    FEMALE = (2, "female")
    OTHER = (3, "other")

    def __new__(cls, id: int, name: str):
        obj = object.__new__(cls)
        obj._value_ = id
        obj.gender_id = id
        obj.gender_name = name
        return obj


class StatusInvoiceEnum(Enum):
    UNFINISHED = (1, "unfinished")
    COMPLETED = (2, "completed")

    def __new__(cls, id: int, name: str):
        obj = object.__new__(cls)
        obj.status_id = id
        obj.status_name = name
        return obj


class DefaultRoleEnum(Enum):
    ADMIN = (1, "admin")
    DOCTOR = (2, "doctor")
    PATIENT = (3, "patient")

    def __new__(cls, id: int, name: str):
        obj = object.__new__(cls)
        obj.role_id = id
        obj.role_name = name
        return obj
