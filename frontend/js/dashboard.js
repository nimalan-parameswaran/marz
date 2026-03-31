const report = JSON.parse(sessionStorage.getItem("last_report"));

if (!report) {
    window.location.href = "visit.html";
}

document.getElementById("patient-name").textContent = report.patient_name;
document.getElementById("patient-age").textContent = report.age + " years";
document.getElementById("diagnosis-output").textContent = report.diagnosis_summary;