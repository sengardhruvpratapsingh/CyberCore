from datetime import datetime

from app.forensic.findings import aggregate_findings


def generate_case_brief(
    case,
    transactions,
    device_records,
    email_artifacts,
    transaction_chains,
    high_value_transactions,
    shared_device_findings,
    email_findings,
    risk_score,
    risk_level,
    risk_signals=None,
    risk_score_maximum=9,
    risk_score_display_denominator=10
):
    """
    One JSON brief covering every evidence type ingested so
    far for the case - the investigator-facing summary the
    build plan calls for alongside the PDF report.
    """

    findings = aggregate_findings(
        transaction_chains=transaction_chains,
        high_value_transactions=high_value_transactions,
        shared_device_findings=shared_device_findings,
        email_findings=email_findings
    )

    return {
        "brief_generated_at": datetime.utcnow(),
        "case": {
            "id": case.id,
            "name": case.name
        },
        "evidence_summary": {
            "total_transactions": len(transactions),
            "total_device_records": len(device_records),
            "total_email_artifacts": len(email_artifacts)
        },
        "risk": {
            "score": risk_score,
            "level": risk_level,
            "signals": risk_signals or [],
            "maximum": risk_score_maximum,
            "display_denominator": risk_score_display_denominator
        },
        "findings": findings,
        "transaction_chains": transaction_chains,
        "high_value_transactions": high_value_transactions,
        "shared_device_findings": shared_device_findings,
        "email_findings": email_findings
    }
