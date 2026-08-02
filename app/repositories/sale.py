from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.sale import Sale

class SaleRepository:
    @staticmethod
    def get_by_id(db: Session, sale_id: int) -> Optional[Sale]:
        return db.query(Sale).filter(Sale.id == sale_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Sale]:
        return db.query(Sale).offset(skip).limit(limit).all()

    @staticmethod
    def create_empty_sale(db: Session, user_id: int, customer_id: Optional[int] = None) -> Sale:
        db_sale = Sale(user_id=user_id, customer_id=customer_id, total_amount=0.0)
        db.add(db_sale)
        db.commit()
        db.refresh(db_sale)
        return db_sale

    @staticmethod
    def update_total(db: Session, sale_id: int, total_amount: float) -> Optional[Sale]:
        db_sale = db.query(Sale).filter(Sale.id == sale_id).first()
        if db_sale:
            db_sale.total_amount = total_amount
            db.commit()
            db.refresh(db_sale)
        return db_sale
