from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.db.postgres import get_db
from backend.models.patient import Patient
from backend.models.visit import Visit
from backend.models.outcome import Outcome

router = APIRouter()

@router.get("/stats/overview")
def get_overview(db: Session = Depends(get_db)):
    total_patients = db.query(func.count(Patient.id)).scalar()
    total_visits = db.query(func.count(Visit.id)).scalar()

    outcomes = db.query(Outcome).all()
    total_outcomes = len(outcomes)
    success = sum(1 for o in outcomes if o.treatment_success == "success")
    partial = sum(1 for o in outcomes if o.treatment_success == "partial")
    failed = sum(1 for o in outcomes if o.treatment_success == "failed")
    success_rate = round((success / total_outcomes * 100)) if total_outcomes > 0 else 0

    recent_visits = (
        db.query(Visit, Patient)
        .join(Patient, Visit.patient_id == Patient.id)
        .order_by(Visit.created_at.desc())
        .limit(5)
        .all()
    )

    return {
        "total_patients": total_patients,
        "total_visits": total_visits,
        "success_rate": success_rate,
        "outcomes": {
            "success": success,
            "partial": partial,
            "failed": failed,
            "total": total_outcomes
        },
        "recent_visits": [
            {
                "patient_name": p.name,
                "visit_id": v.id,
                "symptoms": v.symptoms[:60] + "..." if v.symptoms and len(v.symptoms) > 60 else v.symptoms,
                "date": v.created_at.strftime("%d %b %Y, %H:%M") if v.created_at else "Unknown"
            }
            for v, p in recent_visits
        ]
    }


@router.get("/stats/patient/{name}/trend")
def get_patient_trend(name: str, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(
        Patient.name.ilike(f"%{name}%")
    ).first()

    if not patient:
        return {"error": "Patient not found", "visits": []}

    visits = (
        db.query(Visit)
        .filter(Visit.patient_id == patient.id)
        .order_by(Visit.created_at.asc())
        .all()
    )

    return {
        "patient_name": patient.name,
        "visits": [
            {
                "visit_number": i + 1,
                "date": v.created_at.strftime("%d %b %Y") if v.created_at else f"Visit {i+1}",
                "symptoms": v.symptoms,
                "diagnosis_snippet": v.diagnosis[:120] + "..." if v.diagnosis and len(v.diagnosis) > 120 else v.diagnosis
            }
            for i, v in enumerate(visits)
        ]
    }