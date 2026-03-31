import requests
from backend.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from backend.services.retrieval import retrieve_similar_visits, save_visit_to_memory
import uuid


def generate_report(patient_data: dict) -> dict:
    visit_text = build_visit_text(patient_data)

    past_visits = retrieve_similar_visits(
        current_visit_text=visit_text,
        patient_name=patient_data.get("name", "Unknown")
    )

    prompt = build_prompt(patient_data, past_visits)

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )
    response.raise_for_status()
    report_text = response.json()["response"]

    save_visit_to_memory(
        visit_id=str(uuid.uuid4()),
        patient_name=patient_data.get("name", "Unknown"),
        visit_text=visit_text,
        diagnosis=report_text[:300]
    )

    return {
        "diagnosis_summary": report_text,
        "patient_name": patient_data.get("name"),
        "age": patient_data.get("age"),
    }


def build_visit_text(patient_data: dict) -> str:
    return (
        f"Symptoms: {patient_data.get('symptoms', 'None')}. "
        f"Observations: {patient_data.get('observations', 'None')}. "
        f"Lab results: {patient_data.get('lab_results', 'None')}."
    )


def build_prompt(patient_data: dict, past_visits: list) -> str:
    history_section = ""

    if past_visits:
        history_section = "\n\nPatient's past visit history:\n"
        for i, v in enumerate(past_visits, 1):
            history_section += f"\nVisit {i}:\n  Details: {v['past_visit']}\n  Diagnosis: {v['diagnosis']}\n"
        history_section += "\nUse this history to identify trends or changes in condition.\n"

    return f"""You are a clinical decision support assistant.

Patient details:
- Name: {patient_data.get('name', 'Unknown')}
- Age: {patient_data.get('age', 'Unknown')}
- Symptoms: {patient_data.get('symptoms', 'Not provided')}
- Doctor observations: {patient_data.get('observations', 'Not provided')}
- Lab results: {patient_data.get('lab_results', 'Not provided')}
{history_section}
Task:
1. List the most likely diagnoses with reasoning.
2. Identify any red flag symptoms.
3. Suggest immediate next steps for the doctor.
4. If past visits exist, note any improvement, deterioration, or new concerns.

Be concise and structured."""