import os
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Case
from app.forensic.pdf_report import generate_complete_pdf_report
from app.api.routes.report import get_forensic_report


router = APIRouter(prefix="/cases", tags=["PDF Report"])
REPORT_DIR = Path(__file__).resolve().parents[3] / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/{case_id}/pdf-report")
def download_pdf_report(case_id: int, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    if not case.report_generated:
        raise HTTPException(status_code=409, detail="Generate the report from the Report button first")

    report = get_forensic_report(case_id, db)
    file_name = f"case_{case_id}_forensic_report.pdf"
    file_path = REPORT_DIR / file_name
    generate_complete_pdf_report(file_path=str(file_path), report=report)

    return FileResponse(path=str(file_path), media_type="application/pdf", filename=file_name)
