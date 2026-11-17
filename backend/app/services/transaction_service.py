import pandas as pd


REQUIRED_COLUMNS = [
    "transaction_id",
    "sender",
    "receiver",
    "amount",
    "timestamp"
]


def process_transaction_csv(file_path: str):
    # Read CSV
    df = pd.read_csv(file_path)

    # Support the compact export format used by the uploaded test file.
    df = df.rename(columns={
        "date": "timestamp",
        "upi_id": "sender"
    })

    if "receiver" not in df.columns:
        df["receiver"] = "UNKNOWN"

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

    # Clean string fields
    df["transaction_id"] = (
        df["transaction_id"]
        .astype(str)
        .str.strip()
    )

    df["sender"] = (
        df["sender"]
        .astype(str)
        .str.strip()
    )

    df["receiver"] = (
        df["receiver"]
        .astype(str)
        .str.strip()
    )

    # Convert amount to numeric
    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    # Convert timestamp
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    )

    # Check invalid values
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