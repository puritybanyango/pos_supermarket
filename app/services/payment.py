from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.payment import Payment
from app.models.sale import Sale
from decimal import Decimal

class PaymentService:
    def create(db: Session, sales_id: int, payment_method: str, amount_paid: float):
        if not db.query(Sale).filter(Sale.id == sales_id).first():
            raise HTTPException(status_code=400, detail="Target transaction matching sales_id not found.")
        new_pay = Payment(sales_id=sales_id, payment_method=payment_method, amount_paid=Decimal(str(amount_paid)))
        db.add(new_pay)
        db.commit()
        db.refresh(new_pay)
        return new_pay

    def get_all(db: Session):
        return db.query(Payment).all()

    def update(db: Session, id: int, payment_method: str, amount_paid: float):
        payment = db.query(Payment).filter(Payment.id == id).first()
        if not payment:
            raise HTTPException(status_code=404, detail=f"Payment record matching ID {id} does not exist.")
        
        payment.payment_method = payment_method
        payment.amount_paid = Decimal(str(amount_paid))
        db.commit()
        db.refresh(payment)
        return payment

    def delete(db: Session, id: int):
        payment = db.query(Payment).filter(Payment.id == id).first()
        if not payment:
            raise HTTPException(status_code=404, detail=f"Payment record matching ID {id} does not exist.")
        
        db.delete(payment)
        db.commit()
        return None
