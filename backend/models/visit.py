from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from backend.db.postgres import Base

class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    symptoms = Column(Text, nullable=False)
    observations = Column(Text, nullable=True)
    lab_results = Column(Text, nullable=True)
    diagnosis = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())