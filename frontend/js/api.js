const BASE_URL = "http://localhost:8000/api";

export async function submitVisit(formData) {
    const response = await fetch(`${BASE_URL}/visit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
    });
    if (!response.ok) throw new Error(`Server error: ${response.status}`);
    return await response.json();
}

export async function getPatientHistory(name) {
    const response = await fetch(
        `${BASE_URL}/patient/${encodeURIComponent(name)}/history`
    );
    if (!response.ok) throw new Error(`Server error: ${response.status}`);
    return await response.json();
}

export async function logOutcome(visitId, treatmentSuccess, recoveryNotes) {
    const response = await fetch(`${BASE_URL}/outcome`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            visit_id: visitId,
            treatment_success: treatmentSuccess,
            recovery_notes: recoveryNotes
        })
    });
    if (!response.ok) throw new Error(`Server error: ${response.status}`);
    return await response.json();
}

export async function getOutcome(visitId) {
    const response = await fetch(`${BASE_URL}/outcome/visit/${visitId}`);
    if (!response.ok) throw new Error(`Server error: ${response.status}`);
    return await response.json();
}

export async function getOverviewStats() {
    const response = await fetch(`${BASE_URL}/stats/overview`);
    if (!response.ok) throw new Error(`Server error: ${response.status}`);
    return await response.json();
}

export async function getPatientTrend(name) {
    const response = await fetch(
        `${BASE_URL}/stats/patient/${encodeURIComponent(name)}/trend`
    );
    if (!response.ok) throw new Error(`Server error: ${response.status}`);
    return await response.json();
}