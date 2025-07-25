from app.users.schemas.user import UserCreate
from app.users.schemas.doctor import DoctorCreate
from app.users.schemas.patient import PatientCreate
from app.users.schemas.admin import AdminCreate
from core.common.database import get_async_db_session
from api.common import handlers
from core import services