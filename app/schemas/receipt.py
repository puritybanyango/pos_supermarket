from datetime import datetime
from pydantic import BaseModel, Field

class ReceiptCreate(BaseModel):
    receipt_number: str = Field(..., description="Unique legal audit tracking tracking number reference string.")
    sale_id: int = Field(..., description="Unique structural core matching sale transaction entry link.")

class ReceiptResponse(ReceiptCreate):
    id: int
    issued_at: datetime

    class Config:
        from_attributes = True
