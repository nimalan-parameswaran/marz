from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db.postgres import get_db
from backend.services.report_agent import generate_report
from backend.schemas.visit import VisitCreate, VisitResponse

router = APIRouter()

@router.post("/visit", response_model=VisitResponse)
def create_visit(data: VisitCreate, db: Session = Depends(get_db)):
    report = generate_report(data)   # calls the service
    # save to db ...
    return report