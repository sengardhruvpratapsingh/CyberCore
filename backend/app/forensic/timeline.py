from email.utils import parsedate_to_datetime


def build_case_timeline(
    transactions,
    device_records,
    email_artifacts
):
    """
    Merge every timestamped event across all evidence types
    into one chronological list. Each event keeps its
    evidence type so the investigator knows where it came
    from.
    """

    events = []

    for transaction in transactions:

        events.append({
            "timestamp": transaction.timestamp,
            "event_type": "transaction",
            "type": "financial",
            "entity_ids": [transaction.sender, transaction.receiver],
            "description": (
                f"{transaction.sender} sent "
                f"{transaction.amount} to "
                f"{transaction.receiver}"
            ),
            "summary": f"{transaction.sender} -> {transaction.receiver}",
            "reference": transaction.transaction_id,
            "transaction_id": transaction.transaction_id,
            "amount": transaction.amount,
            "source": "transactions"
        })

    for record in device_records:

        events.append({
            "timestamp": record.timestamp,
            "event_type": "device",
            "type": "device",
            "entity_ids": [record.phone_number, record.imei],
            "description": (
                f"Phone {record.phone_number} observed "
                f"using IMEI {record.imei}"
            ),
            "summary": f"{record.phone_number} linked to IMEI {record.imei}",
            "reference": record.record_id,
            "source": "device records"
        })

    for artifact in email_artifacts:

        parsed_date = None

        if artifact.date_header:

            try:
                parsed_date = parsedate_to_datetime(
                    artifact.date_header
                )

            except (TypeError, ValueError):
                parsed_date = None

        if parsed_date is None:
            continue

        events.append({
            "timestamp": parsed_date,
            "event_type": "email",
            "type": "email",
            "entity_ids": [artifact.from_address, artifact.to_address, artifact.reply_to],
            "description": (
                f"Email from {artifact.from_address} "
                f"to {artifact.to_address}"
            ),
            "summary": "Email header event",
            "reference": artifact.message_id,
            "source": "email artifacts"
        })

    def sort_key(event):

        timestamp = event["timestamp"]

        if timestamp.tzinfo is not None:
            timestamp = timestamp.replace(tzinfo=None)

        return timestamp

    events.sort(key=sort_key)

    return events
