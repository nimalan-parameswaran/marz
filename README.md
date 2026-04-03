# Marz Clinical AI Platform

Marz is a clinical decision support platform that helps healthcare teams document patient visits, generate AI-assisted diagnostic summaries, track treatment outcomes, and review longitudinal patient trends.

It combines a FastAPI backend, PostgreSQL for structured medical records, ChromaDB for visit-memory retrieval, and a lightweight HTML/CSS/JavaScript frontend for clinic workflows.

## 1. Project Title

Marz Clinical AI Platform

## 2. Description

Marz exists to streamline outpatient-style clinical documentation and improve consistency in follow-up decisions.

The system allows clinicians to:

- Capture visit data (symptoms, observations, lab results)
- Generate an AI-supported diagnosis summary using an Ollama-hosted model
- Retrieve similar past visits for the same patient to provide historical context
- Record treatment outcomes (success/partial/failed)
- Monitor high-level performance metrics and patient trends
- Export visit reports as PDFs for sharing or archiving

## 3. Features

- AI-assisted diagnosis generation for new visits
- Retrieval-augmented context from similar previous visits
- Patient history search by name
- Outcome logging and follow-up tracking
- Dashboard with visit/outcome analytics and charts
- Patient trend visualization
- PDF report generation per visit
- Local-first architecture (self-hosted Ollama, PostgreSQL, local Chroma persistence)

## 4. Tech Stack

### Frontend

- HTML5
- CSS3
- Vanilla JavaScript (ES modules)
- Chart.js (for dashboard visualizations)

### Backend

- Python 3
- FastAPI
- Pydantic
- SQLAlchemy
- Requests
- python-dotenv
- ReportLab (PDF generation)

### Database / Data Layer

- PostgreSQL (primary relational store)
- ChromaDB (vector memory for visit similarity retrieval)

### AI / Tooling

- Ollama (local inference and embeddings)
- MedAIBase/MedGemma1.5:4b (default generation model)
- nomic-embed-text (embedding model)

## 5. Project Structure

```text
marz/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── config.py                # Environment variable loading
│   ├── db/
│   │   ├── postgres.py          # SQLAlchemy engine/session/base
│   │   └── chroma.py            # Chroma client/collection access
│   ├── models/                  # SQLAlchemy models (Patient, Visit, Outcome)
│   ├── schemas/                 # Request/response schemas
│   ├── routes/                  # REST API routes
│   │   ├── visits.py
│   │   ├── patients.py
│   │   ├── outcomes.py
│   │   ├── stats.py
│   │   └── reports.py
│   └── services/
│       ├── report_agent.py      # LLM prompt + generation flow
│       ├── retrieval.py         # Chroma save/query logic
│       ├── embeddings.py        # Ollama embedding calls
│       └── pdf_generator.py     # Report PDF rendering
├── frontend/
│   ├── index.html               # Home
│   ├── visit.html               # New visit form
│   ├── history.html             # Patient history + outcomes
│   ├── dashboard.html           # Metrics + trend dashboards
│   ├── css/main.css
│   └── js/
│       ├── api.js               # Frontend API client
│       ├── visit-form.js
│       └── dashboard.js
├── tests/                       # Integration-style test scripts
├── chroma_data/                 # Local Chroma persistence
├── requirements.txt             # Python dependencies (currently empty)
└── README.md
```

## 6. Installation Instructions

### Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Ollama installed and running

### Step-by-step Setup

1. Clone the repository.

```bash
git clone <your-repo-url>
cd marz
```

2. Create and activate a virtual environment.

```bash
python -m venv venv

# Windows PowerShell
venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

3. Install dependencies.

Note: `requirements.txt` is empty in the current project snapshot. Install core packages manually or populate `requirements.txt` first.

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv requests chromadb reportlab
```

4. Prepare PostgreSQL.

- Create a database named `marz` (or use your own name and update `.env`).

5. Start Ollama and pull required models.

```bash
ollama pull MedAIBase/MedGemma1.5:4b
ollama pull nomic-embed-text
```

6. Create your environment file.

Create a `.env` file in the project root using the template in the Environment Variables section.

## 7. Usage Instructions

### Run Backend API

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Health check:

```bash
curl http://localhost:8000/health
```

### Run Frontend

Serve the `frontend` directory on port `5500` (compatible with current CORS settings):

```bash
python -m http.server 5500 --directory frontend
```

Then open:

- `http://localhost:5500/index.html`

### Typical Workflow

1. Open `New Visit` and submit patient details.
2. Review AI-generated diagnosis in the dashboard/report view.
3. Open `Patient History` to inspect previous visits.
4. Record treatment outcomes.
5. Export a PDF report when needed.

## 8. Environment Variables

Create a `.env` file in the project root:

```env
POSTGRES_URL=postgresql://postgres:your_password@localhost/marz
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=MedAIBase/MedGemma1.5:4b
CHROMA_PATH=./chroma_data
```

## 9. API Endpoints

Base URL: `http://localhost:8000/api`

| Method | Endpoint | Description |
|---|---|---|
| POST | `/visit` | Create a patient visit and generate AI diagnosis summary |
| GET | `/patient/{name}/history` | Fetch patient history and prior visit records |
| POST | `/outcome` | Log treatment outcome for a visit |
| GET | `/outcome/visit/{visit_id}` | Get logged outcome for a visit |
| GET | `/stats/overview` | Retrieve aggregate platform metrics and recent activity |
| GET | `/stats/patient/{name}/trend` | Retrieve visit trend timeline for a patient |
| GET | `/report/{visit_id}/pdf` | Download generated PDF report for a visit |

Additional endpoint:

- `GET /health` (system health check)

## 10. Screenshots

Add screenshots to illustrate major screens.

- Home page: `[placeholder] frontend/index.html`
- New visit form: `[placeholder] frontend/visit.html`
- Dashboard analytics: `[placeholder] frontend/dashboard.html`
- Patient history and outcomes: `[placeholder] frontend/history.html`

## 11. Deployment Instructions

Current repository is optimized for local/self-hosted deployment.

### Suggested Production Approach

1. Provision PostgreSQL and persistent storage for `chroma_data`.
2. Deploy Ollama on a machine with sufficient CPU/GPU and keep model artifacts warm.
3. Deploy FastAPI with a production ASGI server:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 2
```

4. Put Nginx or another reverse proxy in front of the API.
5. Serve frontend as static assets (Nginx, CDN, or static host).
6. Restrict CORS origins in `backend/main.py` to your production domains.

## 12. Contributing Guidelines

1. Fork the repository.
2. Create a feature branch.
3. Make focused changes with clear commit messages.
4. Add or update tests where relevant.
5. Submit a pull request with:
	- What changed
	- Why it changed
	- How it was tested

## 13. License

This project is licensed under the MIT License.

## 14. Author / Contact

- Author: NIMALAN
- Email: nimalan936@gmail.com
- Project: Marz Clinical AI Platform

