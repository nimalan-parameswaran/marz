from backend.services.report_agent import generate_report

patient = {
    "name": "Ravi Kumar",
    "age": 45,
    "symptoms": "fatigue, increased thirst, frequent urination",
    "observations": "slightly elevated blood pressure, BMI 28",
    "lab_results": "fasting glucose 210 mg/dL"
}

print("=== FIRST VISIT ===")
result1 = generate_report(patient)
print(result1["diagnosis_summary"][:300])

print("\n=== SECOND VISIT (same patient, follow-up) ===")
patient["symptoms"] = "fatigue reduced, thirst still present, urination normal"
patient["lab_results"] = "fasting glucose 145 mg/dL after medication"
result2 = generate_report(patient)
print(result2["diagnosis_summary"][:300])