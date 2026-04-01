from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db.postgres import get_db
from backend.models.patient import Patient
from backend.models.visit import Visit

router = APIRouter()

@router.get("/patient/{name}/history")
def get_patient_history(name: str, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(
        Patient.name.ilike(f"%{name}%")
    ).first()

    if not patient:
        return {"error": "Patient not found", "visits": []}

    visits = db.query(Visit).filter(
        Visit.patient_id == patient.id
    ).order_by(Visit.created_at.desc()).all()

    return {
        "patient_name": patient.name,
        "age": patient.age,
        "total_visits": len(visits),
        "visits": [
            {
                "visit_id": v.id,
                "date": v.created_at.strftime("%d %b %Y, %H:%M") if v.created_at else "Unknown",
                "symptoms": v.symptoms,
                "observations": v.observations,
                "lab_results": v.lab_results,
                "diagnosis": v.diagnosis
            }
            for v in visits
        ]
    }