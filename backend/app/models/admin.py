from sqlalchemy import Column, Integer, String, DateTime, func
from ..core.database import Base

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)  # will store bcrypt hash
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())