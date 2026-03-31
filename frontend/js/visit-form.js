import { submitVisit } from "./api.js";

const form = document.getElementById("visit-form");
const status = document.getElementById("status");
const submitBtn = document.getElementById("submit-btn");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = {
        patient_name: document.getElementById("patient_name").value,
        age: parseInt(document.getElementById("age").value),
        symptoms: document.getElementById("symptoms").value,
        observations: document.getElementById("observations").value,
        lab_results: document.getElementById("lab_results").value,
    };

    status.className = "status loading";
    status.textContent = "Analysing patient data... this may take 30 seconds.";
    submitBtn.disabled = true;

    try {
        const result = await submitVisit(formData);

        sessionStorage.setItem("last_report", JSON.stringify(result));
        window.location.href = "dashboard.html";

    } catch (err) {
        status.className = "status error";
        status.textContent = "Error: " + err.message;
        submitBtn.disabled = false;
    }
});