from datetime import datetime, timedelta
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Case, Evidence
from app.schemas.case import CaseCreate, CaseResponse


router = APIRouter(
    prefix="/cases",
    tags=["Cases"]
)


def _cleanup_expired_cases(db):
    expiration = datetime.utcnow()
    expired = db.query(Case).filter(
        Case.status == "terminated",
        Case.deletion_at <= expiration
    ).all()
    for case in expired:
        for evidence in db.query(Evidence).filter(
            Evidence.case_id == case.id
        ).all():
            if evidence.file_path:
                Path(evidence.file_path).unlink(missing_ok=True)
        db.delete(case)
    if expired:
        db.commit()


def _serialize_case(case):
    return {
        "id": case.id,
        "name": case.name,
        "case_number": f"CASE-{case.id:04d}",
        "status": case.status,
        "report_generated": case.report_generated,
        "created_at": case.created_at,
        "terminated_at": case.terminated_at,
        "deletion_at": case.deletion_at
    }


@router.get("/", response_model=list[CaseResponse])
def list_cases(
    db: Session = Depends(get_db)
):
    _cleanup_expired_cases(db)
    return [_serialize_case(case) for case in db.query(Case).order_by(Case.id.desc()).all()]


@router.post("/", response_model=CaseResponse)
def create_case(
    case: CaseCreate,
    db: Session = Depends(get_db)
):
    new_case = Case(
        name=case.name
    )

    db.add(new_case)
    db.commit()
    db.refresh(new_case)

    return _serialize_case(new_case)


@router.post("/{case_id}/terminate", response_model=CaseResponse)
def terminate_case(case_id: int, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    if not case.report_generated:
        raise HTTPException(status_code=409, detail="Generate the report before terminating this case")
    if case.status == "terminated":
        return _serialize_case(case)
    case.status = "terminated"
    case.terminated_at = datetime.utcnow()
    case.deletion_at = case.terminated_at + timedelta(days=30)
    db.commit()
    db.refresh(case)
    return _serialize_case(case)


@router.delete("/{case_id}", status_code=204)
def delete_terminated_case(case_id: int, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    if case.status != "terminated":
        raise HTTPException(
            status_code=409,
            detail="Only terminated cases can be permanently deleted"
        )

    for evidence in db.query(Evidence).filter(
        Evidence.case_id == case_id
    ).all():
        if evidence.file_path:
            Path(evidence.file_path).unlink(missing_ok=True)

    db.delete(case)
    db.commit()
    return Response(status_code=204)