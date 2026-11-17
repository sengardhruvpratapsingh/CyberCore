from pydantic import BaseModel
from typing import Optional


class EmailEvidenceResponse(BaseModel):
    id: int
    case_id: int
    filename: str
    sha256: str
    message_id: Optional[str] = None
    from_address: Optional[str] = None
    to_address: Optional[str] = None
    reply_to: Optional[str] = None
    date_header: Optional[str] = None
    source_ip: Optional[str] = None

    class Config:
        from_attributes = True
