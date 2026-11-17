def aggregate_findings(
    transaction_chains,
    high_value_transactions,
    shared_device_findings,
    email_findings
):
    """
    Combine every finding type produced across the financial,
    device and email pipelines into one list the investigator
    can review together.
    """

    findings = []

    if len(transaction_chains) > 0:

        findings.append({
            "type": "TRANSACTION_CHAIN",
            "finding_id": "transaction_chain",
            "title": "Rapid Fund Movement",
            "severity": "HIGH",
            "rule": "rapid_multi_hop",
            "risk_contribution": 2,
            "affected_entities": sorted({entity for chain in transaction_chains for entity in chain.get("path", [])}),
            "source": "transactions",
            "description": (
                f"{len(transaction_chains)} suspicious "
                "transaction chain(s) were identified."
            )
        })

    if len(high_value_transactions) > 0:

        findings.append({
            "type": "HIGH_VALUE_TRANSACTION",
            "finding_id": "high_value_transaction",
            "title": "High-Value Transaction",
            "severity": "HIGH",
            "rule": "high_value_transaction",
            "risk_contribution": 1,
            "affected_entities": sorted({entity for item in high_value_transactions for entity in (item.sender, item.receiver)}),
            "source": "transactions",
            "description": (
                f"{len(high_value_transactions)} high-value "
                "transaction(s) were identified."
            )
        })

    for finding in shared_device_findings:

        findings.append({
            "type": "SHARED_DEVICE",
            "finding_id": "shared_device_association",
            "title": "Shared Device Association",
            "severity": "MEDIUM",
            "rule": "shared_device",
            "risk_contribution": 2,
            "affected_entities": finding.get("phone_numbers", []) + [finding.get("imei")],
            "source": "device records",
            "description": finding["finding"],
            "note": finding["note"]
        })

    for finding in email_findings:

        findings.append({
            "type": "EMAIL_HEADER_MISMATCH",
            "finding_id": "email_header_mismatch",
            "title": "Email Header Inconsistency",
            "severity": "MEDIUM",
            "rule": "email_header_mismatch",
            "risk_contribution": 1,
            "affected_entities": [finding.get("from_address"), finding.get("reply_to")],
            "source": "email artifacts",
            "description": finding["finding"],
            "note": finding["note"]
        })

    if len(findings) == 0:

        findings.append({
            "type": "NO_MAJOR_FINDINGS",
            "finding_id": "no_major_findings",
            "title": "No Major Findings",
            "severity": "LOW",
            "rule": "baseline_review",
            "risk_contribution": 0,
            "affected_entities": [],
            "source": "case evidence",
            "description": (
                "No major suspicious patterns were "
                "identified across the evidence "
                "collected so far."
            )
        })

    return findings
