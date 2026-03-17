from datetime import datetime
from sqlalchemy.orm import Session
from ..models.appointment import Appointment, AppointmentStatus
from ..models.patient import Patient
from ..schemas.appointment import AppointmentCreate, AppointmentSlot
from ..core.security import generate_otp, get_otp_expiry
from . import availability_service

def create_appointment(
    db: Session,
    patient: Patient,
    slot: AppointmentSlot) -> Appointment:
    """Create a new appointment with OTP, after validating slot availability."""
    # Validate slot
    if not availability_service.is_slot_available(db, slot.start_time, slot.end_time):
        raise ValueError("Selected time slot is not available")
    otp = generate_otp()
    otp_expiry = get_otp_expiry()
    db_appointment = Appointment(
        patient_id=patient.id,
        start_time=slot.start_time,
        end_time=slot.end_time,
        status=AppointmentStatus.PENDING,
        otp_code=otp,
        otp_expiry=otp_expiry
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def get_appointment(db: Session, appointment_id: int) -> Appointment | None:
    """Get appointment by ID."""
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()

def cancel_appointment(db: Session, appointment_id: int) -> Appointment | None:
    """Cancel an appointment (status = CANCELLED)."""
    apt = get_appointment(db, appointment_id)
    if apt and apt.status == AppointmentStatus.PENDING:
        apt.status = AppointmentStatus.CANCELLED
        db.commit()
        db.refresh(apt)
    return apt

def verify_otp_and_check_in(db: Session, appointment_id: int, otp: str) -> bool:
    """
    Verify OTP and change status to VISITED if OTP is valid and not expired.
    Returns True if successful.
    """
    apt = get_appointment(db, appointment_id)
    if not apt or apt.status != AppointmentStatus.PENDING:
        return False
    if apt.otp_code != otp:
        return False
    if datetime.utcnow() > apt.otp_expiry:
        return False
    # OTP correct and not expired
    apt.status = AppointmentStatus.VISITED
    db.commit()
    return True

def complete_appointment(db: Session, appointment_id: int) -> Appointment | None:
    """Mark appointment as COMPLETED (admin action)."""
    apt = get_appointment(db, appointment_id)
    if apt and apt.status == AppointmentStatus.VISITED:
        apt.status = AppointmentStatus.COMPLETED
        db.commit()
        db.refresh(apt)
    return apt

def get_appointments_by_patient(db: Session, patient_id: int):
    """Get all appointments for a patient (for history)."""
    return db.query(Appointment).filter(Appointment.patient_id == patient_id).all()