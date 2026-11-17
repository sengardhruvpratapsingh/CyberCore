import json
import re

import pandas as pd
from docx import Document
from pypdf import PdfReader


REQUIRED_COLUMNS = [
    "transaction_id",
    "sender",
    "receiver",
    "amount",
    "timestamp"
]


def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert any structured input into the standard
    CyberCore transaction format.
    """

    # Clean column names
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Check required columns
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Keep only required columns
    df = df[REQUIRED_COLUMNS].copy()

    # Clean string columns
    for column in [
        "transaction_id",
        "sender",
        "receiver"
    ]:
        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
        )

    # Amount
    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    # Timestamp
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    )

    # Validation
    if df["transaction_id"].eq("").any():
        raise ValueError(
            "transaction_id contains empty values"
        )

    if df["sender"].eq("").any():
        raise ValueError(
            "sender contains empty values"
        )

    if df["receiver"].eq("").any():
        raise ValueError(
            "receiver contains empty values"
        )

    if df["amount"].isna().any():
        raise ValueError(
            "amount contains invalid values"
        )

    if df["amount"].lt(0).any():
        raise ValueError(
            "amount cannot be negative"
        )

    if df["timestamp"].isna().any():
        raise ValueError(
            "timestamp contains invalid values"
        )

    return df


def process_csv(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)

    return normalize_dataframe(df)


def process_excel(file_path: str) -> pd.DataFrame:
    df = pd.read_excel(file_path)

    return normalize_dataframe(df)


def process_json(file_path: str) -> pd.DataFrame:
    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

    df = pd.DataFrame(data)

    return normalize_dataframe(df)


def extract_text_from_txt(file_path: str) -> str:
    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:
        return file.read()


def extract_text_from_docx(file_path: str) -> str:
    document = Document(file_path)

    paragraphs = [
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n".join(paragraphs)


def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def extract_transactions_from_text(
    text: str
) -> pd.DataFrame:

    rows = []

    pattern = re.compile(
        r"(?P<transaction_id>\w+)\s*,\s*"
        r"(?P<sender>\w+)\s*,\s*"
        r"(?P<receiver>\w+)\s*,\s*"
        r"(?P<amount>[\d.]+)\s*,\s*"
        r"(?P<timestamp>.+)"
    )

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        match = pattern.match(line)

        if match:

            rows.append({
                "transaction_id":
                    match.group("transaction_id"),

                "sender":
                    match.group("sender"),

                "receiver":
                    match.group("receiver"),

                "amount":
                    match.group("amount"),

                "timestamp":
                    match.group("timestamp")
            })

    if not rows:
        raise ValueError(
            "No transaction records could be extracted from text"
        )

    df = pd.DataFrame(rows)

    return normalize_dataframe(df)


def process_txt(file_path: str) -> pd.DataFrame:
    text = extract_text_from_txt(file_path)

    return extract_transactions_from_text(text)


def process_docx(file_path: str) -> pd.DataFrame:
    text = extract_text_from_docx(file_path)

    return extract_transactions_from_text(text)


def process_pdf(file_path: str) -> pd.DataFrame:
    text = extract_text_from_pdf(file_path)

    if not text.strip():
        raise ValueError(
            "No text could be extracted from PDF"
        )

    return extract_transactions_from_text(text)


def process_file(
    file_path: str,
    filename: str
) -> pd.DataFrame:

    extension = filename.lower().split(".")[-1]

    if extension == "csv":
        return process_csv(file_path)

    elif extension in ["xlsx", "xls"]:
        return process_excel(file_path)

    elif extension == "json":
        return process_json(file_path)

    elif extension == "txt":
        return process_txt(file_path)

    elif extension == "docx":
        return process_docx(file_path)

    elif extension == "pdf":
        return process_pdf(file_path)

    elif extension in ["jpg", "jpeg", "png"]:
        # Import here to avoid circular import.
        from app.forensic.ocr import process_image

        return process_image(file_path)

    else:
        raise ValueError(
            f"Unsupported file format: .{extension}"
        )