from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from ..services import availability_service
from ..api.deps import get_db

router = APIRouter(prefix="/availability", tags=["Availability"])

@router.get("/")
def get_available_slots(
    date: date = Query(..., description="Date to check availability (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Get available appointment slots for a given date."""
    slots = availability_service.get_available_slots(db, date)
    return {"date": date.isoformat(), "slots": slots}