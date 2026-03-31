from backend.services.report_agent import generate_report

fake_patient = {
    "name": "Ravi Kumar",
    "age": 45,
    "symptoms": "fatigue, increased thirst, frequent urination for 3 weeks",
    "observations": "slightly elevated blood pressure, BMI 28",
    "lab_results": "fasting glucose 210 mg/dL"
}

result = generate_report(fake_patient)
print(result["diagnosis_summary"])