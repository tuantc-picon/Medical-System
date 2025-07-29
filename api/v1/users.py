from fastapi import APIRouter, Depends, status, HTTPException
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
@router.post("/register/admin", status_code=status.HTTP_201_CREATED)
async def register_admin(
    admin: AdminCreate,
    db: AsyncSession = Depends(get_async_db_session)
):
    return await Register.admin(admin, db)

@router.post("/register/doctor", status_code=status.HTTP_201_CREATED)
async def register_doctor(
    doctor: DoctorCreate,
    db: AsyncSession = Depends(get_async_db_session)
):
    return await Register.doctor(doctor, db)


@router.post("/register/patient", status_code=status.HTTP_201_CREATED)
async def register_patient(
    patient: PatientCreate,
    db: AsyncSession = Depends(get_async_db_session)
):
    return await Register.patient(patient, db)
