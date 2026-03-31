from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from backend.db.postgres import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=True)
    contact = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())