from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.schemas.visit import VisitCreate, VisitResponse
from backend.services.report_agent import generate_report
from backend.db.postgres import get_db
from backend.models.patient import Patient
from backend.models.visit import Visit

router = APIRouter()

@router.post("/visit", response_model=VisitResponse)
def create_visit(data: VisitCreate, db: Session = Depends(get_db)):

    patient = db.query(Patient).filter(Patient.name == data.patient_name).first()
    if not patient:
        patient = Patient(name=data.patient_name, age=data.age)
        db.add(patient)
        db.commit()
        db.refresh(patient)

    patient_data = {
        "name": data.patient_name,
        "age": data.age,
        "symptoms": data.symptoms,
        "observations": data.observations,
        "lab_results": data.lab_results,
    }
    result = generate_report(patient_data)

    visit = Visit(
        patient_id=patient.id,
        symptoms=data.symptoms,
        observations=data.observations,
        lab_results=data.lab_results,
        diagnosis=result["diagnosis_summary"]
    )
    db.add(visit)
    db.commit()

    return result