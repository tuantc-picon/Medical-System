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


class HTTPMethodsEnum(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


DEFAULT_ROLES = [
    {"id": 1, "name": "admin"},
    {"id": 2, "name": "doctor"},
    {"id": 3, "name": "patient"},
]
