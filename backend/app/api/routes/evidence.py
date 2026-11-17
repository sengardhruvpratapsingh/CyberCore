import hashlib
import os
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File
)
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.database.models import (
    Case,
    Evidence,
    Transaction,
    DeviceRecord,
    EmailArtifact
)

from app.schemas.evidence import EvidenceResponse

from app.forensic.evidence_processor import (
    process_file
)

from app.forensic.device_processor import (
    process_device_file
)

from app.forensic.email_processor import (
    process_eml_file
)
from app.services.evidence_storage import save_evidence_file


router = APIRouter(
    prefix="/cases",
    tags=["Evidence"]
)


BASE_DIR = Path(__file__).resolve().parents[3]
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


ALLOWED_EXTENSIONS = {
    ".csv",
    ".xlsx",
    ".xls",
    ".json",
    ".txt",
    ".docx",
    ".pdf",
    ".eml",
    ".jpg",
    ".jpeg",
    ".png"
}


# Extensions that can carry either transaction data or CDR/
# device data. The uploaded file is sniffed by trying the
# transaction schema first, then the device schema - this is
# what lets a single ingestion endpoint accept "most files"
# without the investigator having to pick a evidence type
# up front, matching the unified-ingestion requirement.
TABULAR_EXTENSIONS = {
    ".csv",
    ".xlsx",
    ".xls",
    ".json"
}


@router.post(
    "/{case_id}/evidence",
    response_model=EvidenceResponse
)
async def upload_evidence(
    case_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # --------------------------------
    # 1. Check case
    # --------------------------------

    case = db.query(Case).filter(
        Case.id == case_id
    ).first()

    if not case:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )
    if case.status == "terminated":
        raise HTTPException(
            status_code=409,
            detail="Cannot upload evidence to a terminated case"
        )

    # --------------------------------
    # 2. Check extension
    # --------------------------------

    extension = os.path.splitext(
        file.filename
    )[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file format. "
                "Allowed: CSV, Excel, JSON, TXT, "
                "DOCX, PDF, EML, JPG, JPEG and PNG"
            )
        )

    # --------------------------------
    # 3. Read file
    # --------------------------------

    file_content = await file.read()

    # --------------------------------
    # 4. SHA-256
    # --------------------------------

    sha256_hash = hashlib.sha256(
        file_content
    ).hexdigest()

    # --------------------------------
    # 5. Save original evidence
    # --------------------------------

    file_path = save_evidence_file(file.filename, file_content)

    # --------------------------------
    # 6. Detect evidence type and process
    #
    # .eml is unambiguous. CSV/Excel/JSON is sniffed by
    # trying the transaction schema first, then the device
    # schema, since both can arrive in the same file types.
    # Everything else stays on the transaction/text path.
    # --------------------------------

    evidence_kind = "transaction"
    transactions_df = None
    device_df = None
    email_headers = None

    try:

        if extension == ".eml":

            email_headers = process_eml_file(str(file_path))
            evidence_kind = "email"

        elif extension in TABULAR_EXTENSIONS:

            try:
                transactions_df = process_file(
                    file_path=str(file_path),
                    filename=file.filename
                )

                evidence_kind = "transaction"

            except ValueError as transaction_error:

                try:
                    device_df = process_device_file(
                        file_path=str(file_path),
                        filename=file.filename
                    )

                    evidence_kind = "device"

                except ValueError:
                    raise transaction_error

        else:

            transactions_df = process_file(
                file_path=str(file_path),
                filename=file.filename
            )

            evidence_kind = "transaction"

    except ValueError as e:

        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    # --------------------------------
    # 7. Save evidence metadata
    # --------------------------------

    evidence = Evidence(
        case_id=case_id,
        filename=file.filename,
        sha256=sha256_hash,
        kind=evidence_kind,
        file_path=str(file_path)
    )

    db.add(evidence)

    # --------------------------------
    # 8. Save the type-specific records
    # --------------------------------

    if evidence_kind == "transaction":

        for _, row in transactions_df.iterrows():

            db.add(Transaction(
                case_id=case_id,
                transaction_id=row["transaction_id"],
                sender=row["sender"],
                receiver=row["receiver"],
                amount=float(row["amount"]),
                timestamp=row["timestamp"]
            ))

    elif evidence_kind == "device":

        for _, row in device_df.iterrows():

            db.add(DeviceRecord(
                case_id=case_id,
                record_id=row["record_id"],
                phone_number=row["phone_number"],
                imei=row["imei"],
                timestamp=row["timestamp"]
            ))

    elif evidence_kind == "email":

        db.add(EmailArtifact(
            case_id=case_id,
            message_id=email_headers["message_id"],
            from_address=email_headers["from_address"],
            to_address=email_headers["to_address"],
            reply_to=email_headers["reply_to"],
            date_header=email_headers["date_header"],
            source_ip=email_headers["source_ip"]
        ))

    # --------------------------------
    # 9. Commit
    # --------------------------------

    db.commit()

    db.refresh(evidence)

    return evidence


@router.get("/{case_id}/evidence")
def list_case_evidence(case_id: int, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    # Older reports generated before report artifacts were persisted are
    # materialized here so terminated cases remain fully inspectable.
    if case.report_generated and not db.query(Evidence).filter(
        Evidence.case_id == case.id,
        Evidence.kind == "report_json"
    ).first():
        from app.api.routes.report import get_forensic_report
        get_forensic_report(case.id, db)

    for item in db.query(Evidence).filter(Evidence.case_id == case.id).all():
        if not item.file_path:
            legacy_path = UPLOAD_DIR / item.filename
            if legacy_path.exists():
                item.file_path = str(legacy_path)
    db.commit()

    return {
        "case_id": case.id,
        "case_number": f"CASE-{case.id:04d}",
        "case_status": case.status,
        "items": [
            {
                "id": item.id,
                "filename": item.filename,
                "kind": item.kind,
                "sha256": item.sha256,
                "uploaded_at": item.uploaded_at,
                "download_url": f"/cases/{case.id}/evidence/{item.id}/download"
            }
            for item in db.query(Evidence)
            .filter(Evidence.case_id == case.id)
            .order_by(Evidence.uploaded_at.desc())
            .all()
        ]
    }


@router.get("/{case_id}/evidence/{evidence_id}/download")
def download_case_evidence(case_id: int, evidence_id: int, db: Session = Depends(get_db)):
    item = db.query(Evidence).filter(
        Evidence.id == evidence_id,
        Evidence.case_id == case_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Evidence item not found")
    if not item.file_path or not Path(item.file_path).exists():
        raise HTTPException(status_code=404, detail="Stored evidence file not found")
    return FileResponse(path=item.file_path, filename=item.filename)
