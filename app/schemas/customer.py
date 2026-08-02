from pydantic import BaseModel, Field

class CustomerBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100, description="Customer's first name.")

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: int

    class Config:
        from_attributes = True
