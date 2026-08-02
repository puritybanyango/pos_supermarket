from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.customer import Customer

class CustomerService:
    @staticmethod
    def create(db: Session, first_name: str, last_name: str, email: str = None, phone: str = None):
        if email and db.query(Customer).filter(Customer.email == email).first():
            raise HTTPException(status_code=400, detail="Customer email profile already registered.")
        new_cust = Customer(first_name=first_name, last_name=last_name, email=email, phone=phone, loyalty_points=0)
        db.add(new_cust)
        db.commit()
        db.refresh(new_cust)
        return new_cust

    @staticmethod
    def get_all(db: Session):
        return db.query(Customer).all()

    @staticmethod
    def get_by_id(db: Session, id: int):
        customer = db.query(Customer).filter(Customer.id == id).first()
        if not customer:
            raise HTTPException(status_code=404, detail=f"Customer record matching ID {id} does not exist.")
        return customer

    @staticmethod
    def update(db: Session, id: int, first_name: str, last_name: str, phone: str = None):
        customer = db.query(Customer).filter(Customer.id == id).first()
        if not customer:
            raise HTTPException(status_code=404, detail=f"Customer record matching ID {id} does not exist.")
        customer.first_name = first_name
        customer.last_name = last_name
        customer.phone = phone
        db.commit()
        db.refresh(customer)
        return customer

    @staticmethod
    def delete(db: Session, id: int):
        customer = db.query(Customer).filter(Customer.id == id).first()
        if not customer:
            raise HTTPException(status_code=404, detail=f"Customer record matching ID {id} does not exist.")
        db.delete(customer)
        db.commit()
        return None
