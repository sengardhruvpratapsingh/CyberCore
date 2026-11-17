from datetime import datetime
import hashlib
import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.routes.case_overview import _compute_all_findings, _load_all_evidence
from app.database.database import get_db
from app.database.models import Case, Evidence
from app.forensic.findings import aggregate_findings
from app.forensic.timeline import build_case_timeline
from app.forensic.unified_graph import build_unified_graph, serialize_unified_graph
from app.forensic.pdf_report import generate_complete_pdf_report


router = APIRouter(prefix="/cases", tags=["Forensic Report"])
REPORT_DIR = Path(__file__).resolve().parents[3] / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def _persist_report_artifacts(case, report, db):
    json_path = REPORT_DIR / f"case_{case.id}_forensic_report.json"
    pdf_path = REPORT_DIR / f"case_{case.id}_forensic_report.pdf"
    json_bytes = json.dumps(report, default=str, indent=2).encode("utf-8")
    json_path.write_bytes(json_bytes)
    generate_complete_pdf_report(file_path=str(pdf_path), report=report)

    artifacts = [
        (json_path, "JSON", json_bytes),
        (pdf_path, "PDF", pdf_path.read_bytes())
    ]
    for path, kind, content in artifacts:
        existing = db.query(Evidence).filter(
            Evidence.case_id == case.id,
            Evidence.kind == f"report_{kind.lower()}"
        ).first()
        if existing:
            existing.file_path = str(path)
            existing.sha256 = hashlib.sha256(content).hexdigest()
            existing.uploaded_at = datetime.utcnow()
            continue
        db.add(Evidence(
            case_id=case.id,
            filename=path.name,
            sha256=hashlib.sha256(content).hexdigest(),
            kind=f"report_{kind.lower()}",
            file_path=str(path)
        ))


@router.get("/{case_id}/report")
def get_forensic_report(case_id: int, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    transactions, device_records, email_artifacts = _load_all_evidence(case_id, db)
    data = _compute_all_findings(case_id, db)
    findings = aggregate_findings(
        transaction_chains=data["chains"],
        high_value_transactions=data["high_value"],
        shared_device_findings=data["shared_devices"],
        email_findings=data["email_findings"]
    )
    graph = serialize_unified_graph(build_unified_graph(
        transactions, device_records, email_artifacts
    ))

    report = {
        "report_generated_at": datetime.utcnow(),
        "case": {
            "id": case.id,
            "case_number": f"CASE-{case.id:04d}",
            "name": case.name,
            "created_at": case.created_at,
            "status": case.status
        },
        "evidence": [
            {"id": item.id, "filename": item.filename, "sha256": item.sha256, "uploaded_at": item.uploaded_at}
            for item in case.evidence
        ],
        "summary": {
            "total_transactions": len(transactions),
            "total_device_records": len(device_records),
            "total_email_artifacts": len(email_artifacts),
            "total_entities": graph["total_nodes"],
            "total_connections": graph["total_edges"],
            "risk_score": data["risk_score"],
            "risk_level": data["risk_level"]
        },
        "timeline": build_case_timeline(transactions, device_records, email_artifacts),
        "findings": findings,
        "entities": graph["nodes"],
        "unified_graph": graph,
        "transaction_chains": data["chains"],
        "high_value_transactions": data["high_value"],
        "shared_device_findings": data["shared_devices"],
        "email_findings": data["email_findings"]
    }

    case.report_generated = True
    _persist_report_artifacts(case, report, db)
    db.commit()
    return report
