import hashlib
import os

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File
)

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.database.models import (
    Case,
    Evidence,
    DeviceRecord
)

from app.schemas.device import DeviceEvidenceResponse

from app.forensic.device_processor import (
    process_device_file
)

from app.forensic.device_correlation import (
    find_shared_devices
)
from app.services.evidence_storage import save_evidence_file


router = APIRouter(
    prefix="/cases",
    tags=["Device Correlation"]
)


UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


ALLOWED_EXTENSIONS = {
    ".csv",
    ".xlsx",
    ".xls"
}


@router.post(
    "/{case_id}/device-evidence",
    response_model=DeviceEvidenceResponse
)
async def upload_device_evidence(
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
                "Unsupported device evidence format. "
                "Allowed: CSV, XLS and XLSX"
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
    # 6. Process file
    # --------------------------------

    try:

        df = process_device_file(
            file_path=str(file_path),
            filename=file.filename
        )

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
        kind="device",
        file_path=str(file_path)
    )

    db.add(evidence)

    # --------------------------------
    # 8. Save device records
    # --------------------------------

    for _, row in df.iterrows():

        device_record = DeviceRecord(
            case_id=case_id,
            record_id=row["record_id"],
            phone_number=row["phone_number"],
            imei=row["imei"],
            timestamp=row["timestamp"]
        )

        db.add(device_record)

    # --------------------------------
    # 9. Commit
    # --------------------------------

    db.commit()

    db.refresh(evidence)

    return {
        "id": evidence.id,
        "case_id": evidence.case_id,
        "filename": evidence.filename,
        "sha256": evidence.sha256,
        "records_ingested": len(df)
    }


@router.get("/{case_id}/device-correlation")
def get_device_correlation(
    case_id: int,
    db: Session = Depends(get_db)
):

    case = db.query(Case).filter(
        Case.id == case_id
    ).first()

    if not case:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    device_records = db.query(DeviceRecord).filter(
        DeviceRecord.case_id == case_id
    ).all()

    findings = find_shared_devices(device_records)

    return {
        "case_id": case_id,
        "total_device_records": len(device_records),
        "shared_device_findings": findings
    }
