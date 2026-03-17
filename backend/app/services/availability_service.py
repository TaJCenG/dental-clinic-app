from datetime import date, datetime, timedelta

from sqlalchemy.orm import Session

from .. import schemas
from ..models.appointment import Appointment, AppointmentStatus
from ..models.staff_availability import StaffAvailability


def get_available_slots(db: Session, target_date: date, slot_duration_minutes: int = 30) -> list[dict]:
    print(f"Fetching available slots for {target_date}")
    availability = db.query(StaffAvailability).filter(
        StaffAvailability.date == target_date,
        StaffAvailability.is_available == True
    ).first()
    if not availability:
        print("No availability record")
        return []
    start_dt = datetime.combine(target_date, availability.start_time)
    end_dt = datetime.combine(target_date, availability.end_time)
    booked = db.query(Appointment).filter(
        Appointment.start_time >= start_dt,
        Appointment.end_time <= end_dt,
        Appointment.status.in_([AppointmentStatus.PENDING, AppointmentStatus.VISITED, AppointmentStatus.COMPLETED])
    ).all()
    booked_intervals = [(apt.start_time, apt.end_time) for apt in booked]
    print(f"Booked intervals: {booked_intervals}")
    slots = []
    current = start_dt
    while current + timedelta(minutes=slot_duration_minutes) <= end_dt:
        slot_end = current + timedelta(minutes=slot_duration_minutes)
        is_available = True
        for b_start, b_end in booked_intervals:
            if not (slot_end <= b_start or current >= b_end):
                is_available = False
                break
        if is_available:
            slots.append({"start": current.isoformat(), "end": slot_end.isoformat()})
        current = slot_end
    print(f"Available slots: {slots}")
    return slots

def is_slot_available(db: Session, start_time: datetime, end_time: datetime) -> bool:
    print(f"Checking slot: {start_time} - {end_time}")
    date = start_time.date()
    availability = db.query(StaffAvailability).filter(
        StaffAvailability.date == date,
        StaffAvailability.is_available == True
    ).first()
    if not availability:
        print("❌ No availability record for this date")
        return False

    day_start = datetime.combine(date, availability.start_time)
    day_end = datetime.combine(date, availability.end_time)
    print(f"Working hours: {day_start} - {day_end}")

    if start_time < day_start or end_time > day_end:
        print("❌ Slot outside working hours")
        return False

    # Check for conflicting appointments
    conflicting = db.query(Appointment).filter(
        Appointment.start_time < end_time,
        Appointment.end_time > start_time,
        Appointment.status.in_([AppointmentStatus.PENDING, AppointmentStatus.VISITED, AppointmentStatus.COMPLETED])
    ).first()
    if conflicting:
        print(f"❌ Conflicting appointment: {conflicting.id} ({conflicting.start_time} - {conflicting.end_time})")
        return False

    print("✅ Slot is available")
    return True

def create_availability(db: Session, avail_data: schemas.staff_availability.StaffAvailabilityCreate) -> StaffAvailability:
    db_avail = StaffAvailability(**avail_data.model_dump())
    db.add(db_avail)
    db.commit()
    db.refresh(db_avail)
    return db_avail

def get_availability_list(db: Session, skip: int = 0, limit: int = 100) -> list[StaffAvailability]:
    return db.query(StaffAvailability).offset(skip).limit(limit).all()

def update_availability(db: Session, avail_id: int, update: schemas.staff_availability.StaffAvailabilityUpdate) -> StaffAvailability | None:
    db_avail = db.query(StaffAvailability).filter(StaffAvailability.id == avail_id).first()
    if not db_avail:
        return None
    update_data = update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_avail, field, value)
    db.commit()
    db.refresh(db_avail)
    return db_avail

def delete_availability(db: Session, avail_id: int) -> bool:
    db_avail = db.query(StaffAvailability).filter(StaffAvailability.id == avail_id).first()
    if not db_avail:
        return False
    db.delete(db_avail)
    db.commit()
    return True