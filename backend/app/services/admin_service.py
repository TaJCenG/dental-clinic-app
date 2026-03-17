from sqlalchemy.orm import Session
from ..models.admin import Admin
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_admin_by_username(db: Session, username: str) -> Admin | None:
    return db.query(Admin).filter(Admin.username == username).first()

def authenticate_admin(db: Session, username: str, password: str) -> Admin | None:
    admin = get_admin_by_username(db, username)
    if not admin:
        return None
    if not pwd_context.verify(password, admin.password_hash):
        return None
    return admin

def create_admin(db: Session, username: str, password: str) -> Admin:
    hashed = pwd_context.hash(password)
    db_admin = Admin(username=username, password_hash=hashed)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin