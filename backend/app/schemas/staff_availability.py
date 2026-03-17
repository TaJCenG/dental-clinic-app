from pydantic import BaseModel
from datetime import date, time, datetime
from typing import Optional

class StaffAvailabilityBase(BaseModel):
    date: date
    start_time: time
    end_time: time
    is_available: bool = True
    reason_blocked: Optional[str] = None

class StaffAvailabilityCreate(StaffAvailabilityBase):
    pass

class StaffAvailabilityUpdate(BaseModel):
    is_available: Optional[bool] = None
    reason_blocked: Optional[str] = None

class StaffAvailability(StaffAvailabilityBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True