from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.supplier import Supplier

class SupplierRepository:
    @staticmethod
    def get_by_id(db: Session, supplier_id: int) -> Optional[Supplier]:
        return db.query(Supplier).filter(Supplier.id == supplier_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Supplier]:
        return db.query(Supplier).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, name: str) -> Supplier:
        db_supplier = Supplier(name=name)
        db.add(db_supplier)
        db.commit()
        db.refresh(db_supplier)
        return db_supplier
