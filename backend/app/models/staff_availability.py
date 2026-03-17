from sqlalchemy import Column, Integer, Date, Time, Boolean, String, DateTime, func
from ..core.database import Base

class StaffAvailability(Base):
    __tablename__ = "staff_availability"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_available = Column(Boolean, default=True)
    reason_blocked = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())