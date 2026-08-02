import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.receipt import Receipt
from app.models.sale import Sale

class ReceiptService:
    def create(db: Session, sale_id: int):
        sale = db.query(Sale).filter(Sale.id == sale_id).first()
        if not sale:
            raise HTTPException(status_code=404, detail=f"Sale matching ID {sale_id} does not exist.")
            
        existing = db.query(Receipt).filter(Receipt.sale_id == sale_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="A receipt has already been issued for this sale.")
            
        receipt_token = f"REC-{uuid.uuid4().hex[:12].upper()}"
        new_receipt = Receipt(sale_id=sale_id, receipt_code=receipt_token)
        
        db.add(new_receipt)
        db.commit()
        db.refresh(new_receipt)
        return new_receipt

    def get_all(db: Session):
        return db.query(Receipt).all()

    def get_by_sale_id(db: Session, sale_id: int):
        receipt = db.query(Receipt).filter(Receipt.sale_id == sale_id).first()
        if not receipt:
            raise HTTPException(status_code=404, detail="No matching receipt found for this sale ID.")
        return receipt

    def update_code(db: Session, id: int, new_code: str):
        receipt = db.query(Receipt).filter(Receipt.id == id).first()
        if not receipt:
            raise HTTPException(status_code=404, detail=f"Receipt record matching ID {id} does not exist.")
            
        receipt.receipt_code = new_code
        db.commit()
        db.refresh(receipt)
        return receipt

    def delete(db: Session, id: int):
        receipt = db.query(Receipt).filter(Receipt.id == id).first()
        if not receipt:
            raise HTTPException(status_code=404, detail=f"Receipt record matching ID {id} does not exist.")
            
        db.delete(receipt)
        db.commit()
        return None
