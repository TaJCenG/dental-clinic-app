from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.database import engine, Base
from .models import *
from .api import availability, patients, appointments  # import routers

# Create database tables (if not already)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dental Clinic API", version="0.1.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(availability.router)
app.include_router(patients.router)
app.include_router(appointments.router)

@app.get("/")
def root():
    return {"message": "Dental Clinic API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

from .api import admin
app.include_router(admin.router)

from .api import availability_admin
app.include_router(availability_admin.router)