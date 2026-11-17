from pydantic import BaseModel


class DeviceEvidenceResponse(BaseModel):
    id: int
    case_id: int
    filename: str
    sha256: str
    records_ingested: int

    class Config:
        from_attributes = True
