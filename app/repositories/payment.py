from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.payment import Payment

class PaymentRepository:
    @staticmethod
    def get_by_id(db: Session, payment_id: int) -> Optional[Payment]:
        return db.query(Payment).filter(Payment.id == payment_id).first()

    @staticmethod
    def get_by_sale_id(db: Session, sale_id: int) -> List[Payment]:
        return db.query(Payment).filter(Payment.sale_id == sale_id).all()

    @staticmethod
    def create(db: Session, payment_method: str, amount_paid: float, sale_id: int) -> Payment:
        db_payment = Payment(payment_method=payment_method, amount_paid=amount_paid, sale_id=sale_id)
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
        return db_payment
