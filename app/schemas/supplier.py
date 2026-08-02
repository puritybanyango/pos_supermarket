from pydantic import BaseModel, Field

class SupplierBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=150, description="Commercial name of the supplier.")

class SupplierCreate(SupplierBase):
    pass

class SupplierResponse(SupplierBase):
    id: int

    class Config:
        from_attributes = True
