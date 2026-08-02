from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from app.models.product import Product
from app.models.category import Category
from app.models.supplier import Supplier
from app.schemas import ProductCreate, ProductResponse
from decimal import Decimal

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(sku: str, name: str, price: float, cost_price: float, stock_qty: int, category_id: int, supplier_id: int, description: str = None, db: Session = Depends(get_db)):
    if db.query(Product).filter(Product.sku == sku).first():
        raise HTTPException(status_code=400, detail="SKU code already assigned to an entry.")
    
    # Preventing invalid database records as required by your prompt instructions
    if not db.query(Category).filter(Category.id == category_id).first():
        raise HTTPException(status_code=400, detail=f"Category matching ID {category_id} does not exist.")
    if not db.query(Supplier).filter(Supplier.id == supplier_id).first():
        raise HTTPException(status_code=400, detail=f"Supplier matching ID {supplier_id} does not exist.")
        
    new_prod = Product(sku=sku, name=name, description=description, price=Decimal(str(price)), cost_price=Decimal(str(cost_price)), stock_qty=stock_qty, category_id=category_id, supplier_id=supplier_id)
    db.add(new_prod)
    db.commit()
    db.refresh(new_prod)
    return new_prod

@router.get("/")
def get_all_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.get("/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product record matching ID {id} does not exist.")
    return product

@router.put("/{id}")
def update_product(id: int, name: str, price: float, cost_price: float, stock_qty: int, db: Session = Depends(get_db)):
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

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product record matching ID {id} does not exist.")
    db.delete(product)
    db.commit()
    return None
