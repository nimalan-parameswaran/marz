const BASE_URL = "http://localhost:8000/api";

export async function submitVisit(formData) {
    const response = await fetch(`${BASE_URL}/visit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
    });

    if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
    }

    return await response.json();
}

export async function getPatientHistory(name) {
    const response = await fetch(`${BASE_URL}/patient/${encodeURIComponent(name)}/history`);

    if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
    }

    return await response.json();
}