from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.schemas.doctor import DoctorCreate
from app.users.schemas.patient import PatientCreate
from app.users.schemas.admin import AdminCreate
from core.services.register import Register

from . import get_async_db_session

router = APIRouter(
    prefix="/v1/users",
    tags=["Register"]
)
@router.post("/register/admin", response_model= AdminCreate, status_code=status.HTTP_201_CREATED)
async def register_admin(
    admin: AdminCreate,
    db: AsyncSession = Depends(get_async_db_session)
):
    db_register = Register(db)
    return await db_register.admin(admin)

@router.post("/register/doctor", response_model= DoctorCreate, status_code=status.HTTP_201_CREATED)
async def register_doctor(
    doctor: DoctorCreate,
    db: AsyncSession = Depends(get_async_db_session)
):
    db_register = Register(db)
    return await db_register.doctor(doctor)


@router.post("/register/patient", response_model= PatientCreate, status_code=status.HTTP_201_CREATED)
async def register_patient(
    patient: PatientCreate,
    db: AsyncSession = Depends(get_async_db_session)
):
    db_register = Register(db)
    return await db_register.patient(patient)