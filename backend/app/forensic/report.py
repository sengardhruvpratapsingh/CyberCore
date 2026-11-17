from datetime import datetime


def generate_forensic_report(
    case,
    transactions,
    chains,
    high_value_transactions,
    risk_score,
    risk_level
):
    report = {
        "report_generated_at": datetime.utcnow(),
        "case": {
            "id": case.id,
            "name": case.name
        },
        "summary": {
            "total_transactions": len(transactions),
            "total_transaction_chains": len(chains),
            "total_high_value_transactions": len(
                high_value_transactions
            ),
            "risk_score": risk_score,
            "risk_level": risk_level
        },
        "transaction_chains": chains,
        "high_value_transactions": high_value_transactions,
        "findings": []
    }

    # Finding 1: Transaction chains
    if len(chains) > 0:
        report["findings"].append({
            "type": "TRANSACTION_CHAIN",
            "severity": "HIGH",
            "description": (
                f"{len(chains)} suspicious transaction "
                "chain(s) were identified."
            )
        })

    # Finding 2: High-value transactions
    if len(high_value_transactions) > 0:
        report["findings"].append({
            "type": "HIGH_VALUE_TRANSACTION",
            "severity": "HIGH",
            "description": (
                f"{len(high_value_transactions)} "
                "high-value transaction(s) were identified."
            )
        })

    # No suspicious findings
    if len(report["findings"]) == 0:
        report["findings"].append({
            "type": "NO_MAJOR_FINDINGS",
            "severity": "LOW",
            "description": (
                "No major suspicious transaction patterns "
                "were identified."
            )
        })

    return report