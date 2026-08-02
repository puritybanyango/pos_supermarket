from pydantic import BaseModel, Field

class SaleItemBase(BaseModel):
    product_id: int = Field(..., description="Target stock product lookup point ID.")
    quantity: int = Field(..., gt=0, description="Total dynamic units items purchased.")

class SaleItemCreate(SaleItemBase):
    pass

class SaleItemResponse(SaleItemBase):
    id: int
    sale_id: int
    unit_price: float = Field(..., description="Snapshotted price locked down at checkout timestamp.")

    class Config:
        from_attributes = True
