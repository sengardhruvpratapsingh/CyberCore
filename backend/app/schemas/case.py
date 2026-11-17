from pydantic import BaseModel


class CaseCreate(BaseModel):
    name: str


class CaseResponse(BaseModel):
    id: int
    name: str
    case_number: str
    status: str
    report_generated: bool
    created_at: object
    terminated_at: object | None = None
    deletion_at: object | None = None

    class Config:
        from_attributes = True