from typing import Optional
from sqlalchemy.orm import Session
from app.models.receipt import Receipt

class ReceiptRepository:
    @staticmethod
    def get_by_id(db: Session, receipt_id: int) -> Optional[Receipt]:
        return db.query(Receipt).filter(Receipt.id == receipt_id).first()

    @staticmethod
    def get_by_number(db: Session, receipt_number: str) -> Optional[Receipt]:
        return db.query(Receipt).filter(Receipt.receipt_number == receipt_number).first()

    @staticmethod
    def create(db: Session, receipt_number: str, sale_id: int) -> Receipt:
        db_receipt = Receipt(receipt_number=receipt_number, sale_id=sale_id)
        db.add(db_receipt)
        db.commit()
        db.refresh(db_receipt)
        return db_receipt
