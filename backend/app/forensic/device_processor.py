import json
import pandas as pd


REQUIRED_COLUMNS = [
    "record_id",
    "phone_number",
    "imei",
    "timestamp"
]


def normalize_device_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert any structured CDR/device input into the standard
    CyberCore device-record format.
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
        "record_id",
        "phone_number",
        "imei"
    ]:
        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
        )

    # Timestamp
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    )

    # Validation
    if df["record_id"].eq("").any():
        raise ValueError(
            "record_id contains empty values"
        )

    if df["phone_number"].eq("").any():
        raise ValueError(
            "phone_number contains empty values"
        )

    if df["imei"].eq("").any():
        raise ValueError(
            "imei contains empty values"
        )

    if df["timestamp"].isna().any():
        raise ValueError(
            "timestamp contains invalid values"
        )

    return df


def process_device_csv(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)

    return normalize_device_dataframe(df)


def process_device_excel(file_path: str) -> pd.DataFrame:
    df = pd.read_excel(file_path)

    return normalize_device_dataframe(df)


def process_device_json(file_path: str) -> pd.DataFrame:
    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

    df = pd.DataFrame(data)

    return normalize_device_dataframe(df)


def process_device_file(
    file_path: str,
    filename: str
) -> pd.DataFrame:

    extension = filename.lower().split(".")[-1]

    if extension == "csv":
        return process_device_csv(file_path)

    elif extension in ["xlsx", "xls"]:
        return process_device_excel(file_path)

    elif extension == "json":
        return process_device_json(file_path)

    else:
        raise ValueError(
            f"Unsupported device evidence format: .{extension}. "
            "CDR/device records must be CSV or Excel."
        )
