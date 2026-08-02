from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.product import Product
from app.models.category import Category
from app.models.supplier import Supplier
from decimal import Decimal

class ProductService:
    @staticmethod
    def create(db: Session, sku: str, name: str, price: float, cost_price: float, stock_qty: int, category_id: int, supplier_id: int, description: str = None):
        if db.query(Product).filter(Product.sku == sku).first():
            raise HTTPException(status_code=400, detail="SKU code already assigned to an entry.")
        
        if not db.query(Category).filter(Category.id == category_id).first():
            raise HTTPException(status_code=400, detail=f"Category matching ID {category_id} does not exist.")
        if not db.query(Supplier).filter(Supplier.id == supplier_id).first():
            raise HTTPException(status_code=400, detail=f"Supplier matching ID {supplier_id} does not exist.")
            
        new_prod = Product(sku=sku, name=name, description=description, price=Decimal(str(price)), cost_price=Decimal(str(cost_price)), stock_qty=stock_qty, category_id=category_id, supplier_id=supplier_id)
        db.add(new_prod)
        db.commit()
        db.refresh(new_prod)
        return new_prod

    @staticmethod
    def get_all(db: Session):
        return db.query(Product).all()

    @staticmethod
    def get_by_id(db: Session, id: int):
        product = db.query(Product).filter(Product.id == id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product record matching ID {id} does not exist.")
        return product

    @staticmethod
    def update(db: Session, id: int, name: str, price: float, cost_price: float, stock_qty: int):
        product = db.query(Product).filter(Product.id == id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product record matching ID {id} does not exist.")
        product.name = name
        product.price = Decimal(str(price))
        product.cost_price = Decimal(str(cost_price))
        product.stock_qty = stock_qty
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def delete(db: Session, id: int):
        product = db.query(Product).filter(Product.id == id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product record matching ID {id} does not exist.")
        db.delete(product)
        db.commit()
        return None
