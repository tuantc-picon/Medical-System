from core.schemas.base import MSBaseSchema, MSTimestamp
from datetime import datetime


class DoctorCertificate(MSBaseSchema):
    doctor_id : int
    certificate_id : int

class Certificates(MSBaseSchema):
    certificate_id : int
    created_archive: datetime
    certificate_name : str