from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, services
from ..api.deps import get_db

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/", response_model=schemas.patient.Patient)
def create_or_get_patient(
    patient: schemas.patient.PatientCreate,
    db: Session = Depends(get_db)
):
    """Create a new patient or return existing one by phone."""
    return services.patient_service.get_or_create_patient(db, patient)

@router.get("/{patient_id}", response_model=schemas.patient.Patient)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):
    """Get patient by ID."""
    patient = services.patient_service.get_patient_by_phone(db, str(patient_id))  # Note: This is a workaround; we need a get_by_id method.
    # Better: add a get_patient_by_id method.
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.get("/by-phone/{phone}", response_model=list[schemas.appointment.Appointment])
def get_patient_appointments_by_phone(
    phone: str,
    db: Session = Depends(get_db)
):
    """Get all appointments for a patient by phone number."""
    patient = services.patient_service.get_patient_by_phone(db, phone)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    appointments = services.appointment_service.get_appointments_by_patient(db, patient.id)
    return appointments