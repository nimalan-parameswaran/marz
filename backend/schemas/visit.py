from pydantic import BaseModel
from typing import Optional

class VisitCreate(BaseModel):
    patient_name: str
    age: int
    symptoms: str
    observations: Optional[str] = None
    lab_results: Optional[str] = None

class VisitResponse(BaseModel):
    patient_name: str
    age: int
    diagnosis_summary: str

    class Config:
        from_attributes = True