from PIL import Image
import pytesseract

from app.forensic.evidence_processor import (
    extract_transactions_from_text
)


def process_image(file_path: str):

    image = Image.open(file_path)

    text = pytesseract.image_to_string(
        image
    )

    if not text.strip():
        raise ValueError(
            "No text could be extracted from image"
        )

    return extract_transactions_from_text(
        text
    )