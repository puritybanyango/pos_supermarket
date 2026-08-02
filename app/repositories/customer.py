from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.customer import Customer

class CustomerRepository:
    @staticmethod
    def get_by_id(db: Session, customer_id: int) -> Optional[Customer]:
        return db.query(Customer).filter(Customer.id == customer_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Customer]:
        return db.query(Customer).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, first_name: str) -> Customer:
        db_customer = Customer(first_name=first_name)
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer
