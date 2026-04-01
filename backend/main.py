from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import visits, patients, outcomes, stats
from backend.db.postgres import create_tables
from backend.models import patient, visit, outcome

app = FastAPI(title="Marz Clinical AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    create_tables()

app.include_router(visits.router, prefix="/api")
app.include_router(patients.router, prefix="/api")
app.include_router(outcomes.router, prefix="/api")
app.include_router(stats.router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok", "system": "marz"}