from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AdminBase(BaseModel):
    username: str

class AdminCreate(AdminBase):
    password: str  # plain password

class AdminLogin(AdminBase):
    password: str

class Admin(AdminBase):
    id: int
    last_login: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True