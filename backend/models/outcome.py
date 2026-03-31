from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from backend.db.postgres import Base

class Outcome(Base):
    __tablename__ = "outcomes"

    id = Column(Integer, primary_key=True, index=True)
    visit_id = Column(Integer, ForeignKey("visits.id"), nullable=False)
    treatment_success = Column(String, nullable=True)
    recovery_notes = Column(Text, nullable=True)
    recorded_at = Column(DateTime, default=func.now())