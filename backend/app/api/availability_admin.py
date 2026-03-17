from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, services
from ..api.deps import get_db, get_current_admin

router = APIRouter(prefix="/admin/availability", tags=["Admin Availability"], dependencies=[Depends(get_current_admin)])

@router.post("/", response_model=schemas.staff_availability.StaffAvailability, status_code=201)
def create_availability(
    availability: schemas.staff_availability.StaffAvailabilityCreate,
    db: Session = Depends(get_db)
):
    """Create a new availability slot or block."""
    db_avail = services.availability_service.create_availability(db, availability)
    return db_avail

@router.get("/", response_model=list[schemas.staff_availability.StaffAvailability])
def list_availability(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all availability records."""
    return services.availability_service.get_availability_list(db, skip, limit)

@router.put("/{avail_id}", response_model=schemas.staff_availability.StaffAvailability)
def update_availability(
    avail_id: int,
    update: schemas.staff_availability.StaffAvailabilityUpdate,
    db: Session = Depends(get_db)
):
    """Update an availability record (e.g., block/unblock)."""
    db_avail = services.availability_service.update_availability(db, avail_id, update)
    if not db_avail:
        raise HTTPException(status_code=404, detail="Availability record not found")
    return db_avail

@router.delete("/{avail_id}", status_code=204)
def delete_availability(avail_id: int, db: Session = Depends(get_db)):
    """Delete an availability record."""
    success = services.availability_service.delete_availability(db, avail_id)
    if not success:
        raise HTTPException(status_code=404, detail="Availability record not found")
    return None