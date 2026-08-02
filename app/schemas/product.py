from typing import Optional
from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    sku: str = Field(..., min_length=3, max_length=50, description="Unique Stock Keeping Unit barcode.")
    name: str = Field(..., min_length=2, max_length=200, description="Commercial name of the product.")
    description: Optional[str] = Field(None, max_length=500, description="Product description specifications.")
    price: float = Field(..., gt=0, description="Selling retail price to consumers.")
    cost_price: float = Field(..., gt=0, description="Acquisition wholesale cost price from supplier.")
    stock_qty: int = Field(..., ge=0, description="Remaining real-time inventory count.")
    category_id: int = Field(..., description="Relational link back to structural categories.")
    supplier_id: int = Field(..., description="Relational link back to tracking supplier entity.")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    sku: Optional[str] = None
    name: Optional[str] = None
    price: Optional[float] = None
    cost_price: Optional[float] = None
    stock_qty: Optional[int] = None
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True
