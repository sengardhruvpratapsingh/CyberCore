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

from app.forensic.unified_graph import (
    build_unified_graph,
    serialize_unified_graph
)

from app.forensic.timeline import build_case_timeline

from app.forensic.findings import aggregate_findings

from app.forensic.case_brief import generate_case_brief

from app.schemas.copilot import CopilotQuestion

from app.forensic.copilot import answer_with_router, copilot_status


router = APIRouter(
    prefix="/cases",
    tags=["Case Overview"]
)


def _load_case_or_404(case_id, db):

    case = db.query(Case).filter(
        Case.id == case_id
    ).first()

    if not case:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    return case


def _load_all_evidence(case_id, db):

    transactions = db.query(Transaction).filter(
        Transaction.case_id == case_id
    ).all()

    device_records = db.query(DeviceRecord).filter(
        DeviceRecord.case_id == case_id
    ).all()

    email_artifacts = db.query(EmailArtifact).filter(
        EmailArtifact.case_id == case_id
    ).all()

    return transactions, device_records, email_artifacts


@router.get("/{case_id}/unified-graph")
def get_unified_graph(
    case_id: int,
    db: Session = Depends(get_db)
):

    _load_case_or_404(case_id, db)

    transactions, device_records, email_artifacts = (
        _load_all_evidence(case_id, db)
    )

    graph = build_unified_graph(
        transactions,
        device_records,
        email_artifacts
    )

    return serialize_unified_graph(graph)


@router.get("/{case_id}/timeline")
def get_case_timeline(
    case_id: int,
    db: Session = Depends(get_db)
):

    _load_case_or_404(case_id, db)

    transactions, device_records, email_artifacts = (
        _load_all_evidence(case_id, db)
    )

    events = build_case_timeline(
        transactions,
        device_records,
        email_artifacts
    )

    return {
        "case_id": case_id,
        "total_events": len(events),
        "events": events
    }


def _compute_all_findings(case_id, db):

    transactions, device_records, email_artifacts = (
        _load_all_evidence(case_id, db)
    )

    graph = build_transaction_graph(transactions)

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
        "transactions": transactions,
        "device_records": device_records,
        "email_artifacts": email_artifacts,
        "chains": chains,
        "high_value": high_value,
        "shared_devices": shared_devices,
        "email_findings": email_findings,
        "risk_score": assessment["score"],
        "risk_level": assessment["level"],
        "risk_signals": assessment["signals"],
        "risk_score_maximum": assessment["maximum"],
        "risk_score_display_denominator": assessment["display_denominator"]
    }


@router.get("/{case_id}/findings")
def get_case_findings(
    case_id: int,
    db: Session = Depends(get_db)
):

    case = _load_case_or_404(case_id, db)

    data = _compute_all_findings(case_id, db)

    findings = aggregate_findings(
        transaction_chains=data["chains"],
        high_value_transactions=data["high_value"],
        shared_device_findings=data["shared_devices"],
        email_findings=data["email_findings"]
    )

    return {
        "case_id": case_id,
        "risk_score": data["risk_score"],
        "risk_level": data["risk_level"],
        "risk_signals": data["risk_signals"],
        "risk_score_maximum": data["risk_score_maximum"],
        "risk_score_display_denominator": data["risk_score_display_denominator"],
        "findings": findings
    }


@router.get("/{case_id}/brief")
def get_case_brief(
    case_id: int,
    db: Session = Depends(get_db)
):

    case = _load_case_or_404(case_id, db)

    data = _compute_all_findings(case_id, db)

    return generate_case_brief(
        case=case,
        transactions=data["transactions"],
        device_records=data["device_records"],
        email_artifacts=data["email_artifacts"],
        transaction_chains=data["chains"],
        high_value_transactions=data["high_value"],
        shared_device_findings=data["shared_devices"],
        email_findings=data["email_findings"],
        risk_score=data["risk_score"],
        risk_level=data["risk_level"],
        risk_signals=data["risk_signals"],
        risk_score_maximum=data["risk_score_maximum"],
        risk_score_display_denominator=data["risk_score_display_denominator"]
    )



@router.post("/{case_id}/copilot/ask")
def ask_copilot(
    case_id: int,
    body: CopilotQuestion,
    db: Session = Depends(get_db)
):

    case = _load_case_or_404(case_id, db)

    data = _compute_all_findings(case_id, db)

    result = answer_with_router(
        question=body.question,
        data=data,
        case=case,
    )

    return {
        "case_id": case_id,
        "question": body.question,
        "tool_used": result["tool"],
        "tool": result["tool"],
        "arguments": result["arguments"],
        "answer": result["answer"],
        "result": result["result"],
        "grounded_on": result["grounded_on"],
        "mode": result["mode"],
        "limitations": result["limitations"],
    }


@router.get("/{case_id}/copilot/tools")
def get_copilot_tools(case_id: int, db: Session = Depends(get_db)):
    _load_case_or_404(case_id, db)
    return {"case_id": case_id, **copilot_status()}


@router.get("/{case_id}/entities/{entity_id:path}")
def get_entity_dossier(case_id: int, entity_id: str, db: Session = Depends(get_db)):
    case = _load_case_or_404(case_id, db)
    transactions, device_records, email_artifacts = _load_all_evidence(case_id, db)
    graph = serialize_unified_graph(build_unified_graph(transactions, device_records, email_artifacts))
    matching_edges = [edge for edge in graph["edges"] if entity_id in (str(edge["source"]), str(edge["target"]))]
    if not any(str(node["id"]) == entity_id for node in graph["nodes"]):
        raise HTTPException(status_code=404, detail="Entity not found in this case")

    findings_data = _compute_all_findings(case_id, db)
    findings = aggregate_findings(
        transaction_chains=findings_data["chains"],
        high_value_transactions=findings_data["high_value"],
        shared_device_findings=findings_data["shared_devices"],
        email_findings=findings_data["email_findings"]
    )
    related_transactions = [
        {
            "transaction_id": item.transaction_id,
            "sender": item.sender,
            "receiver": item.receiver,
            "direction": "sent" if item.sender == entity_id else "received",
            "amount": item.amount,
            "timestamp": item.timestamp,
            "source": "transactions"
        }
        for item in transactions if entity_id in (item.sender, item.receiver)
    ]
    related_devices = [
        {
            "record_id": item.record_id,
            "phone_number": item.phone_number,
            "imei": item.imei,
            "timestamp": item.timestamp,
            "source": "device records"
        }
        for item in device_records if entity_id in (item.phone_number, item.imei)
    ]
    related_email = [
        {
            "message_id": item.message_id,
            "from": item.from_address,
            "to": item.to_address,
            "reply_to": item.reply_to,
            "source": "email artifacts"
        }
        for item in email_artifacts if entity_id in (item.from_address, item.to_address, item.reply_to)
    ]
    return {
        "case_id": case_id,
        "case_number": f"CASE-{case_id:04d}",
        "entity": {"id": entity_id, "display_name": entity_id, "type": "Identifier"},
        "risk_score": findings_data["risk_score"],
        "risk_level": findings_data["risk_level"],
        "identifiers": {"value": entity_id},
        "transactions": related_transactions,
        "connected_entities": sorted({
            str(edge["target"] if str(edge["source"]) == entity_id else edge["source"])
            for edge in matching_edges
        }),
        "device_associations": related_devices,
        "email_associations": related_email,
        "findings": findings,
        "evidence": [
            {"id": item.id, "filename": item.filename, "kind": item.kind}
            for item in case.evidence
        ]
    }