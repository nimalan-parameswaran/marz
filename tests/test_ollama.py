import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "MedAIBase/MedGemma1.5:4b",
        "prompt": "Patient has fever and sore throat. List 3 possible diagnoses.",
        "stream": False
    }
)

data = response.json()
print(data["response"])