from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from app.services.receipt import ReceiptService
from app.schemas import ReceiptResponse
from typing import List

router = APIRouter(prefix="/receipts", tags=["Receipt"])

@router.post("/", response_model=ReceiptResponse, status_code=status.HTTP_201_CREATED)
def create_receipt_manually(sale_id: int, db: Session = Depends(get_db)):
    """Manually generates a brand new unique audit receipt tracking code for an existing sale."""
    return ReceiptService.create(db, sale_id)

@router.get("/", response_model=List[ReceiptResponse])
def get_all_receipts(db: Session = Depends(get_db)):
    """Retrieves all receipt compliance logs saved inside the database."""
    return ReceiptService.get_all(db)

@router.get("/{sale_id}", response_model=ReceiptResponse)
def get_receipt_by_sale_id(sale_id: int, db: Session = Depends(get_db)):
    """Retrieves a single receipt row matching a specific Sale primary ID."""
    return ReceiptService.get_by_sale_id(db, sale_id)

@router.put("/{id}", response_model=ReceiptResponse)
def update_receipt_code_string(id: int, new_receipt_code: str, db: Session = Depends(get_db)):
    """Updates the explicit tracking code string of a specific receipt entry using its ID."""
    return ReceiptService.update_code(db, id, new_receipt_code)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_receipt_record(id: int, db: Session = Depends(get_db)):
    """Permanently deletes a specific receipt logging entry from the system database using its ID."""
    return ReceiptService.delete(db, id)
