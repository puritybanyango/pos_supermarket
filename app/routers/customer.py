from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.customer import CustomerCreate
from database import get_db
from app.models.customer import Customer
from app.schemas import CustomerCreate, CustomerResponse
router = APIRouter(prefix="/customers", tags=["Customers"])

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(payload: CustomerCreate, db: Session = Depends(get_db)):
    if payload.email and db.query(Customer).filter(Customer.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Customer email profile already registered.")
    new_cust = Customer(first_name=payload.first_name, last_name=payload.last_name, email=payload.email, phone=payload.phone, loyalty_points=0)
    db.add(new_cust)
    db.commit()
    db.refresh(new_cust)
    return new_cust

@router.get("/")
def get_all_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()

@router.get("/{id}")
def get_customer_by_id(id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == id).first()
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer record matching ID {id} does not exist.")
    return customer

@router.put("/{id}")
def update_customer(id: int, payload: CustomerCreate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == id).first()
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer record matching ID {id} does not exist.")
    customer.first_name = payload.first_name
    customer.last_name = payload.last_name
    customer.phone = payload.phone
    db.commit()
    db.refresh(customer)
    return customer

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == id).first()
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer record matching ID {id} does not exist.")
    db.delete(customer)
    db.commit()
    return None
