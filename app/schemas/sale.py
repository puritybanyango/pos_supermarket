from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

from app.schemas.sale_item import SaleItemCreate, SaleItemResponse

class SaleCreate(BaseModel):
    items: List[SaleItemCreate] = Field(..., min_items=1)
    customer_id: Optional[int] = None
    user_id: int
    discount_amount: Decimal = Field(default=Decimal("0.00"), ge=0)
    tax_rate: Decimal = Field(default=Decimal("0.16"), ge=0)

class SaleResponse(BaseModel):
    id: int
    invoice_number: str
    timestamp: datetime
    subtotal: Decimal
    tax_amount: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    customer_id: Optional[int]
    user_id: int
    items: List[SaleItemResponse] = []

    class Config:
        from_attributes = True
