from pathlib import Path
from uuid import uuid4


UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_evidence_file(filename: str, content: bytes) -> Path:
    safe_name = Path(filename).name
    path = UPLOAD_DIR / f"{uuid4().hex}_{safe_name}"
    path.write_bytes(content)
    return path