from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.schemas.doctor import DoctorCreate
from app.users.schemas.patient import PatientCreate
from app.users.schemas.admin import AdminCreate

from . import services
from . import get_async_db_session

router = APIRouter(
    prefix="/v2/users",
    tags=["Register"]
)
@router.post("/register/admin", status_code=status.HTTP_201_CREATED)
async def register_admin(
    admin: AdminCreate,
    db: AsyncSession = Depends(get_async_db_session)
):
    return await services.register_admin(admin, db)

@router.post("/register/doctor", status_code=status.HTTP_201_CREATED)
async def register_doctor(
    doctor: DoctorCreate,
    db: AsyncSession = Depends(get_async_db_session)
):
    return await services.register_doctor(doctor, db)


@router.post("/register/patient", status_code=status.HTTP_201_CREATED)
async def register_patient(
    patient: PatientCreate,
    db: AsyncSession = Depends(get_async_db_session)
):
    return await services.register_patient(patient, db)


