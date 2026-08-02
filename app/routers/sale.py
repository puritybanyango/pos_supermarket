from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from database import get_db
from app.services.sale import SaleService
from app.schemas import SaleCreate, SaleResponse
from typing import List, Optional

router = APIRouter(prefix="/sales", tags=["Sale"])

@router.post("/", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
def create_sale_transaction(payload: SaleCreate, db: Session = Depends(get_db)):
    """Processes a new checkout line item transaction and automatically handles calculations and stock drops."""
   
    first_item = payload.items[0]
    return SaleService.create(db, first_item.product_id, first_item.quantity, payload.user_id, payload.customer_id, float(payload.discount_amount))

@router.get("/", response_model=List[SaleResponse])
def get_all_sales(db: Session = Depends(get_db)):
    """Retrieves all checkout transaction history rows from the system database."""
    return SaleService.get_all(db)

@router.get("/{id}", response_model=SaleResponse)
def get_sale_by_id(id: int, db: Session = Depends(get_db)):
    """Retrieves a specific sale transaction metadata details record using its ID."""
    return SaleService.get_by_id(db, id)

@router.put("/{id}", response_model=SaleResponse)
def update_sale_metadata(id: int, customer_id: Optional[int] = Query(None), user_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """Modifies the active tracking customer or system user operator assigned to a sale."""
    return SaleService.update_metadata(db, id, customer_id, user_id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def void_sale_transaction(id: int, db: Session = Depends(get_db)):
    """Voids a transaction, returns items to product stock counts, and cascades deletion down to receipts and payments."""
    return SaleService.delete(db, id)
