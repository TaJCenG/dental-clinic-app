from sqlalchemy.orm import Session
from ..models.patient import Patient
from ..schemas.patient import PatientCreate

def get_patient_by_phone(db: Session, phone: str) -> Patient | None:
    """Retrieve a patient by phone number."""
    return db.query(Patient).filter(Patient.phone == phone).first()

def create_patient(db: Session, patient_data: PatientCreate) -> Patient:
    """Create a new patient."""
    db_patient = Patient(**patient_data.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_or_create_patient(db: Session, patient_data: PatientCreate) -> Patient:
    """Get existing patient by phone or create a new one."""
    patient = get_patient_by_phone(db, patient_data.phone)
    if not patient:
        patient = create_patient(db, patient_data)
    return patient

def get_patient_by_id(db: Session, patient_id: int) -> Patient | None:
    return db.query(Patient).filter(Patient.id == patient_id).first()