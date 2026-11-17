from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Case, Transaction

from app.forensic.graph import build_transaction_graph

from app.forensic.patterns import (
    find_transaction_chains,
    find_high_value_transactions
)

from app.forensic.risk import (
    calculate_risk_assessment,
    HIGH_VALUE_THRESHOLD
)


router = APIRouter(
    prefix="/cases",
    tags=["Forensic Analysis"]
)


@router.get("/{case_id}/analysis")
def analyze_case(
    case_id: int,
    db: Session = Depends(get_db)
):

    # 1. Check case
    case = db.query(Case).filter(
        Case.id == case_id
    ).first()

    if not case:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    # 2. Get transactions
    transactions = db.query(Transaction).filter(
        Transaction.case_id == case_id
    ).all()

    # 3. Build graph
    graph = build_transaction_graph(
        transactions
    )

    # 4. Detect transaction chains
    chains = find_transaction_chains(
        graph,
        transactions,
        minimum_length=3
    )

    # 5. Detect high-value transactions
    high_value = find_high_value_transactions(
        transactions,
        threshold=HIGH_VALUE_THRESHOLD
    )

    assessment = calculate_risk_assessment(
        transactions=transactions,
        transaction_chains=chains,
        high_value_transactions=high_value
    )

    return {
        "case_id": case_id,

        "total_transactions": len(
            transactions
        ),

        "total_entities": graph.number_of_nodes(),

        "total_connections": graph.number_of_edges(),

        "transaction_chains": chains,

        "high_value_transactions": high_value,

        "risk_score": assessment["score"],

        "risk_level": assessment["level"],

        "risk_signals": assessment["signals"],

        "risk_score_maximum": assessment["maximum"],

        "risk_score_display_denominator": assessment["display_denominator"]
    }