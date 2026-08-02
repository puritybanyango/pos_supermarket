from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from app.models.sale_item import SaleItem
from app.models.sale import Sale
from app.models.product import Product
from app.schemas import SaleItemCreate, SaleItemResponse
from decimal import Decimal

router = APIRouter(prefix="/sale-items", tags=["Sale Item"])

@router.post("/", response_model=SaleItemResponse, status_code=status.HTTP_201_CREATED)
def create_sale_item(sale_id: int, product_id: int, quantity: int, db: Session = Depends(get_db)):
  
    if not db.query(Sale).filter(Sale.id == sale_id).first():
        raise HTTPException(status_code=400, detail=f"Parent Sale record matching ID {sale_id} does not exist.")
        
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=400, detail=f"Product matching ID {product_id} does not exist.")
    if product.stock_qty < quantity:
        raise HTTPException(status_code=400, detail=f"Insufficient inventory levels. Available stock: {product.stock_qty}")


    unit_price = product.price
    total_price = Decimal(str(unit_price)) * Decimal(str(quantity))

    new_item = SaleItem(
        sale_id=sale_id,
        product_id=product_id,
        quantity=quantity,
        unit_price=unit_price,
        total_price=total_price
    )
    product.stock_qty -= quantity
    
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.get("/")
def get_all_sale_items(db: Session = Depends(get_db)):
    return db.query(SaleItem).all()


@router.get("/{id}")
def get_sale_item_by_id(id: int, db: Session = Depends(get_db)):
    item = db.query(SaleItem).filter(SaleItem.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"Sale Item record matching ID {id} does not exist.")
    return item


@router.put("/{id}")
def update_sale_item_quantity(id: int, new_quantity: int, db: Session = Depends(get_db)):
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


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sale_item(id: int, db: Session = Depends(get_db)):
    item = db.query(SaleItem).filter(SaleItem.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"Sale Item record matching ID {id} does not exist.")
    

    product = db.query(Product).filter(Product.id == item.product_id).first()
    if product:
        product.stock_qty += item.quantity
        
    db.delete(item)
    db.commit()
    return None
