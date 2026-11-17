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
    EmailArtifact
)

from app.schemas.email import EmailEvidenceResponse

from app.forensic.email_processor import (
    process_eml_file
)

from app.forensic.email_analysis import (
    find_email_findings
)
from app.services.evidence_storage import save_evidence_file


router = APIRouter(
    prefix="/cases",
    tags=["Email Analysis"]
)


UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


ALLOWED_EXTENSIONS = {
    ".eml"
}


@router.post(
    "/{case_id}/email-evidence",
    response_model=EmailEvidenceResponse
)
async def upload_email_evidence(
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
            detail="Unsupported format. Only .eml is accepted"
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

        headers = process_eml_file(str(file_path))

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
        kind="email",
        file_path=str(file_path)
    )

    db.add(evidence)

    # --------------------------------
    # 8. Save email artifact
    # --------------------------------

    email_artifact = EmailArtifact(
        case_id=case_id,
        message_id=headers["message_id"],
        from_address=headers["from_address"],
        to_address=headers["to_address"],
        reply_to=headers["reply_to"],
        date_header=headers["date_header"],
        source_ip=headers["source_ip"]
    )

    db.add(email_artifact)

    # --------------------------------
    # 9. Commit
    # --------------------------------

    db.commit()

    db.refresh(evidence)
    db.refresh(email_artifact)

    return {
        "id": evidence.id,
        "case_id": evidence.case_id,
        "filename": evidence.filename,
        "sha256": evidence.sha256,
        "message_id": email_artifact.message_id,
        "from_address": email_artifact.from_address,
        "to_address": email_artifact.to_address,
        "reply_to": email_artifact.reply_to,
        "date_header": email_artifact.date_header,
        "source_ip": email_artifact.source_ip
    }


@router.get("/{case_id}/email-findings")
def get_email_findings(
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

    email_artifacts = db.query(EmailArtifact).filter(
        EmailArtifact.case_id == case_id
    ).all()

    findings = find_email_findings(email_artifacts)

    return {
        "case_id": case_id,
        "total_email_artifacts": len(email_artifacts),
        "email_findings": findings
    }
