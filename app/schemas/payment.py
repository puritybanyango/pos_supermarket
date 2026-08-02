from datetime import datetime
from pydantic import BaseModel, Field

class PaymentCreate(BaseModel):
    payment_method: str = Field(..., description="Tender method validation parameters (CASH, CARD, MOBILE).")
    amount_paid: float = Field(..., gt=0, description="Total liquidity received count parameter.")
    sale_id: int = Field(..., description="Relational target checkout event manifest transaction.")

class PaymentResponse(PaymentCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
