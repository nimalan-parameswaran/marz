from fastapi import APIRouter
from backend.schemas.visit import VisitCreate, VisitResponse
from backend.services.report_agent import generate_report

router = APIRouter()

@router.post("/visit", response_model=VisitResponse)
def create_visit(data: VisitCreate):
    patient_data = {
        "name": data.patient_name,
        "age": data.age,
        "symptoms": data.symptoms,
        "observations": data.observations,
        "lab_results": data.lab_results,
    }
    result = generate_report(patient_data)
    return result