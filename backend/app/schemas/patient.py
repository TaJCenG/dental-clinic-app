from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PatientBase(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(PatientBase):
    pass

class Patient(PatientBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True