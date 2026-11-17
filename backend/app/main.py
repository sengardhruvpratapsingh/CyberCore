from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine
from app.database import models
from sqlalchemy import inspect, text

from app.api.routes import cases
from app.api.routes import evidence
from app.api.routes import device
from app.api.routes import email
from app.api.routes import case_overview
from app.api.routes import transactions
from app.api.routes import forensic
from app.api.routes import risk
from app.api.routes import report
from app.api.routes import pdf_report


Base.metadata.create_all(bind=engine)

# Keep the local SQLite database usable after adding lifecycle fields.
with engine.begin() as connection:
    columns = {column["name"] for column in inspect(engine).get_columns("cases")}
    for name, definition in {
        "status": "VARCHAR DEFAULT 'active' NOT NULL",
        "report_generated": "BOOLEAN DEFAULT 0 NOT NULL",
        "terminated_at": "DATETIME",
        "deletion_at": "DATETIME"
    }.items():
        if name not in columns:
            connection.execute(text(f"ALTER TABLE cases ADD COLUMN {name} {definition}"))

    evidence_columns = {column["name"] for column in inspect(engine).get_columns("evidence")}
    for name, definition in {
        "kind": "VARCHAR DEFAULT 'case_document' NOT NULL",
        "file_path": "VARCHAR"
    }.items():
        if name not in evidence_columns:
            connection.execute(text(f"ALTER TABLE evidence ADD COLUMN {name} {definition}"))


app = FastAPI(title="CyberCore Backend")

# Allow the static frontend (Live Server/file://) to call the local API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(cases.router)
app.include_router(evidence.router)
app.include_router(device.router)
app.include_router(email.router)
app.include_router(case_overview.router)
app.include_router(transactions.router)
app.include_router(forensic.router)
app.include_router(risk.router)
app.include_router(report.router)
app.include_router(pdf_report.router)


@app.get("/")
def home():
    return {
        "status": "ok",
        "message": "CyberCore Backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }