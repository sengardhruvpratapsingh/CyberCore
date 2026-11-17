from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import (
    Case,
    Transaction,
    DeviceRecord,
    EmailArtifact
)

from app.forensic.graph import build_transaction_graph

from app.forensic.patterns import (
    find_transaction_chains,
    find_high_value_transactions
)

from app.forensic.device_correlation import find_shared_devices

from app.forensic.email_analysis import find_email_findings

from app.forensic.risk import (
    calculate_risk_assessment,
    HIGH_VALUE_THRESHOLD
)


router = APIRouter(
    prefix="/cases",
    tags=["Risk Scoring"]
)


@router.get("/{case_id}/risk")
def get_case_risk(
    case_id: int,
    db: Session = Depends(get_db)
):

    # Check case
    case = db.query(Case).filter(
        Case.id == case_id
    ).first()

    if not case:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    # Get transactions
    transactions = db.query(Transaction).filter(
        Transaction.case_id == case_id
    ).all()

    device_records = db.query(DeviceRecord).filter(
        DeviceRecord.case_id == case_id
    ).all()

    email_artifacts = db.query(EmailArtifact).filter(
        EmailArtifact.case_id == case_id
    ).all()

    # Build graph
    graph = build_transaction_graph(
        transactions
    )

    # Detect patterns
    chains = find_transaction_chains(
        graph,
        transactions,
        minimum_length=3
    )

    high_value = find_high_value_transactions(
        transactions,
        threshold=HIGH_VALUE_THRESHOLD
    )

    shared_devices = find_shared_devices(device_records)
    email_findings = find_email_findings(email_artifacts)

    assessment = calculate_risk_assessment(
        transactions=transactions,
        transaction_chains=chains,
        high_value_transactions=high_value,
        shared_device_findings=shared_devices,
        email_findings=email_findings,
        device_records=device_records,
        email_artifacts=email_artifacts
    )

    return {
        "case_id": case_id,
        "risk_score": assessment["score"],
        "risk_level": assessment["level"],
        "risk_signals": assessment["signals"],
        "risk_score_maximum": assessment["maximum"],
        "risk_score_display_denominator": assessment["display_denominator"]
    }