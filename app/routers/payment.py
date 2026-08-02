from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from app.services.payment import PaymentService
from app.schemas import PaymentCreate, PaymentResponse
from typing import List

router = APIRouter(prefix="/payments", tags=["Payment"])

@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def add_payment(payload: PaymentCreate, db: Session = Depends(get_db)):
    """Records a new payment for a sale transaction."""
    return PaymentService.create(db, payload.sales_id, payload.payment_method, payload.amount_paid)

@router.get("/", response_model=List[PaymentResponse])
def get_all_payments(db: Session = Depends(get_db)):
    """Retrieves all historical payment records."""
    return PaymentService.get_all(db)

@router.put("/{id}", response_model=PaymentResponse)
def update_payment(id: int, payment_method: str, amount_paid: float, db: Session = Depends(get_db)):
    """Updates an existing payment's method or amount using its ID."""
    return PaymentService.update(db, id, payment_method, amount_paid)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(id: int, db: Session = Depends(get_db)):
    """Permanently removes a payment record from the database using its ID."""
    return PaymentService.delete(db, id)
