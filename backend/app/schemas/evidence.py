from pydantic import BaseModel


class EvidenceResponse(BaseModel):
    id: int
    case_id: int
    filename: str
    sha256: str
    kind: str = "case_document"
    file_path: str | None = None
    uploaded_at: object | None = None

    class Config:
        from_attributes = True