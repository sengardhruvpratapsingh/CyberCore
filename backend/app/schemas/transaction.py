from pydantic import BaseModel
from datetime import datetime


class TransactionResponse(BaseModel):
    id: int
    case_id: int
    transaction_id: str
    sender: str
    receiver: str
    amount: float
    timestamp: datetime

    class Config:
        from_attributes = True