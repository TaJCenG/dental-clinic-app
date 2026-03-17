from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, services
from ..api.deps import get_db

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.post("/", response_model=schemas.appointment.Appointment, status_code=status.HTTP_201_CREATED)
def create_appointment(
    booking: schemas.appointment.AppointmentBookingRequest,
    db: Session = Depends(get_db)
):
    try:
        patient = services.patient_service.get_or_create_patient(db, booking.patient)
        new_apt = services.appointment_service.create_appointment(db, patient, booking.slot)
        return new_apt
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    """
    Book a new appointment.
    Provide patient details and the desired time slot.
    Returns the created appointment with OTP.
    """
    # 1. Get or create patient
    patient = services.patient_service.get_or_create_patient(db, booking.patient)
    # 2. Create appointment with OTP
    new_apt = services.appointment_service.create_appointment(db, patient, booking.slot)
    return new_apt

@router.post("/{appointment_id}/cancel")
def cancel_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    """Cancel a pending appointment."""
    apt = services.appointment_service.cancel_appointment(db, appointment_id)
    if not apt:
        raise HTTPException(status_code=404, detail="Appointment not found or cannot be cancelled")
    return {"message": "Appointment cancelled", "appointment": apt}

@router.post("/{appointment_id}/check-in")
def check_in(
    appointment_id: int,
    otp: str,
    db: Session = Depends(get_db)
):
    """Verify OTP and mark appointment as VISITED."""
    success = services.appointment_service.verify_otp_and_check_in(db, appointment_id, otp)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid OTP or appointment cannot be checked in")
    return {"message": "Check-in successful"}

@router.post("/{appointment_id}/complete")
def complete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    """Mark appointment as COMPLETED (admin only later)."""
    apt = services.appointment_service.complete_appointment(db, appointment_id)
    if not apt:
        raise HTTPException(status_code=404, detail="Appointment not found or cannot be completed")
    return {"message": "Appointment completed", "appointment": apt}

@router.get("/patient/{patient_id}")
def get_patient_appointments(
    patient_id: int,
    db: Session = Depends(get_db)
):
    """Get all appointments for a patient."""
    appointments = services.appointment_service.get_appointments_by_patient(db, patient_id)
    return appointments

@router.post("/{appointment_id}/reschedule")
def reschedule_appointment(
    appointment_id: int,
    new_slot: schemas.appointment.AppointmentSlot,
    db: Session = Depends(get_db)
):
    """Reschedule a pending appointment to a new time slot."""
    # Get the appointment
    apt = services.appointment_service.get_appointment(db, appointment_id)
    if not apt or apt.status != AppointmentStatus.PENDING:
        raise HTTPException(status_code=404, detail="Appointment not found or cannot be rescheduled")
    # Validate new slot availability
    if not services.availability_service.is_slot_available(db, new_slot.start_time, new_slot.end_time):
        raise HTTPException(status_code=400, detail="New slot is not available")
    # Cancel old appointment
    services.appointment_service.cancel_appointment(db, appointment_id)
    # Create new appointment with same patient
    new_apt = services.appointment_service.create_appointment(db, apt.patient, new_slot)
    return new_apt