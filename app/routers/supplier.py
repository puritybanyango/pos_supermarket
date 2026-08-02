from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from app.models.supplier import Supplier
from app.schemas import SupplierCreate, SupplierResponse

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

@router.post("/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(payload: SupplierCreate, db: Session = Depends(get_db)):
    new_sup = Supplier(company_name=payload.company_name, contact_name=payload.contact_name, phone=payload.phone, email=payload.email)
    db.add(new_sup)
    db.commit()
    db.refresh(new_sup)
    return new_sup

@router.get("/")
def get_all_suppliers(db: Session = Depends(get_db)):
    return db.query(Supplier).all()

@router.get("/{id}")
def get_supplier_by_id(id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.id == id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail=f"Supplier record matching ID {id} does not exist.")
    return supplier

@router.put("/{id}")
def update_supplier(id: int, company_name: str, phone: str, contact_name: str = None, email: str = None, db: Session = Depends(get_db)):
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

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.id == id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail=f"Supplier record matching ID {id} does not exist.")
    db.delete(supplier)
    db.commit()
    return None
