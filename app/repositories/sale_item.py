from typing import List
from sqlalchemy.orm import Session
from app.models.sale_item import SaleItem

class SaleItemRepository:
    @staticmethod
    def get_by_sale_id(db: Session, sale_id: int) -> List[SaleItem]:
        return db.query(SaleItem).filter(SaleItem.sale_id == sale_id).all()
