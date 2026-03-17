from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum
from .patient import PatientCreate   # or from ..schemas import PatientCreate
from .. import schemas


class AppointmentStatus(str, Enum):
    PENDING = "pending"
    VISITED = "visited"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class AppointmentBase(BaseModel):
    patient_id: int
    start_time: datetime
    end_time: datetime
    status: AppointmentStatus = AppointmentStatus.PENDING

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    status: Optional[AppointmentStatus] = None
    # other fields if needed

class Appointment(AppointmentBase):
    id: int
    otp_code: str
    otp_expiry: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AppointmentSlot(BaseModel):
    start_time: datetime
    end_time: datetime


class AppointmentBookingRequest(BaseModel):
    patient: schemas.patient.PatientCreate
    slot: AppointmentSlot

# Add this to the existing file
class AppointmentAdminView(BaseModel):
    id: int
    patient_id: int
    patient_name: str
    patient_phone: str
    start_time: datetime
    end_time: datetime
    status: AppointmentStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True