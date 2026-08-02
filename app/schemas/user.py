from pydantic import BaseModel, Field

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Unique login handle identifier.")
    role: str = Field("cashier", description="Security clearance tier parameter (admin, manager, cashier).")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Plain text password payload.")

class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
