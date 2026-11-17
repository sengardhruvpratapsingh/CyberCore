import re
from email import policy
from email.parser import BytesParser


IP_PATTERN = re.compile(
    r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
)


def extract_source_ip(received_headers):
    """
    Best-effort extraction of a source IP from the Received
    headers. Header parsing only - no deep mail-server
    trust chain validation.
    """

    for header in received_headers:

        match = IP_PATTERN.search(header)

        if match:
            return match.group(0)

    return None


def process_eml_file(file_path: str) -> dict:
    """
    Extract header fields from a .eml file:
    From, To, Reply-To, Date, Message-ID, Received / Source IP.

    Header parsing only - no MIME body or attachment parsing,
    per the hackathon build plan.
    """

    with open(file_path, "rb") as f:
        raw_bytes = f.read()

    raw_bytes = raw_bytes.lstrip(b"\xef\xbb\xbf")
    message = BytesParser(policy=policy.default).parsebytes(raw_bytes)

    received_headers = message.get_all("Received", [])

    received_headers = [
        str(header)
        for header in received_headers
    ]

    from_address = message.get("From")
    to_address = message.get("To")
    reply_to = message.get("Reply-To")
    date_header = message.get("Date")
    message_id = message.get("Message-ID")

    if not from_address:
        raise ValueError(
            "No From header found in .eml file"
        )

    return {
        "message_id": message_id,
        "from_address": str(from_address),
        "to_address": str(to_address) if to_address else None,
        "reply_to": str(reply_to) if reply_to else None,
        "date_header": str(date_header) if date_header else None,
        "source_ip": extract_source_ip(received_headers)
    }
