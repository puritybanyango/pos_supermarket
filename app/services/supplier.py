from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.supplier import Supplier

class SupplierService:
    @staticmethod
    def create(db: Session, company_name: str, phone: str, contact_name: str = None, email: str = None):
        new_sup = Supplier(company_name=company_name, contact_name=contact_name, phone=phone, email=email)
        db.add(new_sup)
        db.commit()
        db.refresh(new_sup)
        return new_sup

    @staticmethod
    def get_all(db: Session):
        return db.query(Supplier).all()

    @staticmethod
    def get_by_id(db: Session, id: int):
        supplier = db.query(Supplier).filter(Supplier.id == id).first()
        if not supplier:
            raise HTTPException(status_code=404, detail=f"Supplier record matching ID {id} does not exist.")
        return supplier

    @staticmethod
    def update(db: Session, id: int, company_name: str, phone: str, contact_name: str = None, email: str = None):
        supplier = db.query(Supplier).filter(Supplier.id == id).first()
        if not supplier:
            raise HTTPException(status_code=404, detail=f"Supplier record matching ID {id} does not exist.")
        supplier.company_name = company_name
        supplier.contact_name = contact_name
        supplier.phone = phone
        supplier.email = email
        db.commit()
        db.refresh(supplier)
        return supplier

    @staticmethod
    def delete(db: Session, id: int):
        supplier = db.query(Supplier).filter(Supplier.id == id).first()
        if not supplier:
            raise HTTPException(status_code=404, detail=f"Supplier record matching ID {id} does not exist.")
        db.delete(supplier)
        db.commit()
        return None
