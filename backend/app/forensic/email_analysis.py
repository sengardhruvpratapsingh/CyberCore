from email.utils import parseaddr


def find_email_findings(email_artifacts):
    """
    Rule: From != Reply-To.

    Only the address portion is compared (a display name
    like "Support <billing@bank.com>" should not trigger a
    false mismatch against the same address written plainly).

    This never confirms spoofing on its own - it is an
    observed header inconsistency only. Stronger conclusions
    require additional evidence.
    """

    findings = []

    for artifact in email_artifacts:

        if not artifact.reply_to:
            continue

        _, from_email = parseaddr(artifact.from_address or "")
        _, reply_to_email = parseaddr(artifact.reply_to)

        if not from_email or not reply_to_email:
            continue

        if from_email.lower() != reply_to_email.lower():

            findings.append({
                "email_artifact_id": artifact.id,
                "message_id": artifact.message_id,
                "from_address": artifact.from_address,
                "reply_to": artifact.reply_to,
                "finding": "From/Reply-To mismatch observed.",
                "association_type": "observed",
                "note": (
                    "This does not confirm spoofing. "
                    "Stronger conclusions require additional "
                    "evidence."
                )
            })

    return findings
