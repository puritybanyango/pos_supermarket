import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.product import Product
from app.models.user import User
from app.models.customer import Customer
from app.models.receipt import Receipt
from decimal import Decimal

class SaleService:
    def create(db: Session, product_id: int, quantity: int, user_id: int, customer_id: int = None, discount: float = 0.0):
        if not db.query(User).filter(User.id == user_id).first():
            raise HTTPException(status_code=400, detail="User processing checkout does not exist.")
        if customer_id and not db.query(Customer).filter(Customer.id == customer_id).first():
            raise HTTPException(status_code=400, detail="Linked loyalty customer profile not found.")
            
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=400, detail=f"Product with ID {product_id} does not exist.")
        if product.stock_qty < quantity:
            raise HTTPException(status_code=400, detail=f"Deficit stock allocation. Available: {product.stock_qty}")

        subtotal = Decimal(str(product.price)) * Decimal(str(quantity))
        discount_amount = Decimal(str(discount))
        tax_amount = (subtotal - discount_amount) * Decimal("0.10")
        total_amount = (subtotal - discount_amount) + tax_amount

        invoice_code = f"INV-{uuid.uuid4().hex[:8].upper()}"
        new_sale = Sale(invoice_number=invoice_code, subtotal=subtotal, tax_amount=tax_amount, discount_amount=discount_amount, total_amount=total_amount, customer_id=customer_id, user_id=user_id)
        db.add(new_sale)
        db.flush()

        product.stock_qty -= quantity
        new_item = SaleItem(sale_id=new_sale.id, product_id=product_id, quantity=quantity, unit_price=product.price, total_price=subtotal)
        db.add(new_item)

        new_receipt = Receipt(sale_id=new_sale.id, receipt_code=f"REC-{uuid.uuid4().hex[:12].upper()}")
        db.add(new_receipt)

        db.commit()
        db.refresh(new_sale)
        return new_sale

    def get_all(db: Session):
        return db.query(Sale).all()

    def get_by_id(db: Session, id: int):
        sale = db.query(Sale).filter(Sale.id == id).first()
        if not sale:
            raise HTTPException(status_code=404, detail=f"Sale transaction record matching ID {id} does not exist.")
        return sale

    def update_metadata(db: Session, id: int, customer_id: int = None, user_id: int = None):
        sale = db.query(Sale).filter(Sale.id == id).first()
        if not sale:
            raise HTTPException(status_code=404, detail=f"Sale transaction record matching ID {id} does not exist.")
        
        if customer_id:
            if not db.query(Customer).filter(Customer.id == customer_id).first():
                raise HTTPException(status_code=400, detail="Linked loyalty customer profile not found.")
            sale.customer_id = customer_id
            
        if user_id:
            if not db.query(User).filter(User.id == user_id).first():
                raise HTTPException(status_code=400, detail="User executing transaction does not exist.")
            sale.user_id = user_id

        db.commit()
        db.refresh(sale)
        return sale

    def delete(db: Session, id: int):
        sale = db.query(Sale).filter(Sale.id == id).first()
        if not sale:
            raise HTTPException(status_code=404, detail=f"Sale transaction record matching ID {id} does not exist.")
        
        # Give allocated item quantities back to product stock inventories before hard deletion
        for item in sale.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if product:
                product.stock_qty += item.quantity
                
        db.delete(sale)
        db.commit()
        return None
