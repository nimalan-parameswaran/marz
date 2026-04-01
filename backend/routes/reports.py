from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
from backend.db.postgres import get_db
from backend.models.visit import Visit
from backend.models.patient import Patient
from backend.models.outcome import Outcome
from backend.services.pdf_generator import build_pdf

router = APIRouter()

@router.get("/report/{visit_id}/pdf")
def download_report(visit_id: int, db: Session = Depends(get_db)):
    visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if not visit:
        return Response(content="Visit not found", status_code=404)

    patient = db.query(Patient).filter(
        Patient.id == visit.patient_id
    ).first()

    outcome = db.query(Outcome).filter(
        Outcome.visit_id == visit_id
    ).first()

    visit_data = {
        "visit_id":     visit.id,
        "patient_name": patient.name if patient else "Unknown",
        "age":          patient.age if patient else "—",
        "gender":       patient.gender if patient else None,
        "symptoms":     visit.symptoms,
        "observations": visit.observations,
        "lab_results":  visit.lab_results,
        "diagnosis":    visit.diagnosis,
        "outcome": {
            "treatment_success": outcome.treatment_success,
            "recovery_notes":    outcome.recovery_notes,
        } if outcome else None,
    }

    pdf_bytes = build_pdf(visit_data)
    filename = f"marz_report_visit_{visit_id}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )