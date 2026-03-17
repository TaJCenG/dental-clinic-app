from http.client import HTTPException
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.appointment import Appointment, AppointmentStatus
from ..api.deps import get_db, get_current_admin
from ..schemas.admin import AdminLogin, AdminCreate, Admin
from ..services import admin_service

from ..core.security import create_access_token
from datetime import timedelta
from ..core.config import settings
from sqlalchemy.orm import joinedload
from ..schemas.appointment import AppointmentAdminView

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard/stats", dependencies=[Depends(get_current_admin)])
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Return counts of appointments by status."""
    total = db.query(func.count(Appointment.id)).scalar()
    visited = db.query(func.count(Appointment.id)).filter(Appointment.status == AppointmentStatus.VISITED).scalar()
    completed = db.query(func.count(Appointment.id)).filter(Appointment.status == AppointmentStatus.COMPLETED).scalar()
    cancelled = db.query(func.count(Appointment.id)).filter(Appointment.status == AppointmentStatus.CANCELLED).scalar()
    pending = db.query(func.count(Appointment.id)).filter(Appointment.status == AppointmentStatus.PENDING).scalar()

    return {
        "total": total or 0,
        "visited": visited or 0,
        "completed": completed or 0,
        "cancelled": cancelled or 0,
        "pending": pending or 0
    }


@router.post("/login")
def admin_login(login_data: AdminLogin, db: Session = Depends(get_db)):
    admin = admin_service.authenticate_admin(db, login_data.username, login_data.password)
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": admin.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/create-admin")
def create_admin_user(admin: AdminCreate, db: Session = Depends(get_db)):
    """Temporary endpoint to create an admin user (remove after initial setup)."""
    existing = admin_service.get_admin_by_username(db, admin.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_admin = admin_service.create_admin(db, admin.username, admin.password)
    return {"message": "Admin created", "username": new_admin.username}



@router.get("/appointments", response_model=list[AppointmentAdminView])
def get_all_appointments(
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin)
):
    """Get all appointments with patient details (admin only)."""
    appointments = db.query(Appointment).options(
        joinedload(Appointment.patient)
    ).order_by(Appointment.start_time.desc()).all()

    return [
        {
            "id": apt.id,
            "patient_id": apt.patient_id,
            "patient_name": apt.patient.name,
            "patient_phone": apt.patient.phone,
            "start_time": apt.start_time,
            "end_time": apt.end_time,
            "status": apt.status,
            "created_at": apt.created_at,
            "updated_at": apt.updated_at,
        }
        for apt in appointments
    ]