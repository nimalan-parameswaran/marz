from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from backend.db.postgres import get_db
from backend.models.outcome import Outcome
from backend.models.visit import Visit

router = APIRouter()

class OutcomeCreate(BaseModel):
    visit_id: int
    treatment_success: str
    recovery_notes: Optional[str] = None

@router.post("/outcome")
def log_outcome(data: OutcomeCreate, db: Session = Depends(get_db)):
    visit = db.query(Visit).filter(Visit.id == data.visit_id).first()

    if not visit:
        return {"error": "Visit not found"}

    outcome = Outcome(
        visit_id=data.visit_id,
        treatment_success=data.treatment_success,
        recovery_notes=data.recovery_notes
    )
    db.add(outcome)
    db.commit()

    return {
        "message": "Outcome recorded successfully",
        "visit_id": data.visit_id,
        "treatment_success": data.treatment_success
    }

@router.get("/outcome/visit/{visit_id}")
def get_outcome(visit_id: int, db: Session = Depends(get_db)):
    outcome = db.query(Outcome).filter(
        Outcome.visit_id == visit_id
    ).first()

    if not outcome:
        return {"message": "No outcome recorded yet"}

    return {
        "visit_id": outcome.visit_id,
        "treatment_success": outcome.treatment_success,
        "recovery_notes": outcome.recovery_notes,
        "recorded_at": outcome.recorded_at.strftime("%d %b %Y") if outcome.recorded_at else None
    }