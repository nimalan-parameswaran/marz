import requests
from backend.config import OLLAMA_BASE_URL, OLLAMA_MODEL

def generate_report(patient_data: dict) -> dict:
    prompt = build_prompt(patient_data)

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

    return {
        "diagnosis_summary": report_text,
        "patient_name": patient_data.get("name"),
        "age": patient_data.get("age"),
    }


def build_prompt(patient_data: dict) -> str:
    return f"""You are a clinical decision support assistant.

Patient details:
- Name: {patient_data.get('name', 'Unknown')}
- Age: {patient_data.get('age', 'Unknown')}
- Symptoms: {patient_data.get('symptoms', 'Not provided')}
- Doctor observations: {patient_data.get('observations', 'Not provided')}
- Lab results: {patient_data.get('lab_results', 'Not provided')}

Task:
1. List the most likely diagnoses with reasoning.
2. Identify any red flag symptoms.
3. Suggest immediate next steps for the doctor.

Be concise and structured."""