from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.sale_item import SaleItem
from app.models.sale import Sale
from app.models.product import Product
from decimal import Decimal

class SaleItemService:
    @staticmethod
    def create(db: Session, sale_id: int, product_id: int, quantity: int):
        if not db.query(Sale).filter(Sale.id == sale_id).first():
            raise HTTPException(status_code=400, detail=f"Parent Sale record matching ID {sale_id} does not exist.")
            
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=400, detail=f"Product matching ID {product_id} does not exist.")
        if product.stock_qty < quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient inventory levels. Available stock: {product.stock_qty}")

        unit_price = product.price
        total_price = Decimal(str(unit_price)) * Decimal(str(quantity))

        new_item = SaleItem(sale_id=sale_id, product_id=product_id, quantity=quantity, unit_price=unit_price, total_price=total_price)
        product.stock_qty -= quantity
        
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item

    @staticmethod
    def get_all(db: Session):
        return db.query(SaleItem).all()

    @staticmethod
    def get_by_id(db: Session, id: int):
        item = db.query(SaleItem).filter(SaleItem.id == id).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"Sale Item record matching ID {id} does not exist.")
        return item

    @staticmethod
    def update(db: Session, id: int, new_quantity: int):
        item = db.query(SaleItem).filter(SaleItem.id == id).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"Sale Item record matching ID {id} does not exist.")
            
        product = db.query(Product).filter(Product.id == item.product_id).first()
        quantity_difference = new_quantity - item.quantity
        if product.stock_qty < quantity_difference:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for this change. Needed: {quantity_difference}")

        product.stock_qty -= quantity_difference
        item.quantity = new_quantity
        item.total_price = Decimal(str(item.unit_price)) * Decimal(str(new_quantity))
        
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete(db: Session, id: int):
        item = db.query(SaleItem).filter(SaleItem.id == id).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"Sale Item record matching ID {id} does not exist.")
        
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stock_qty += item.quantity
            
        db.delete(item)
        db.commit()
        return None
