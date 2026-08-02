from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.category import Category

class CategoryRepository:
    @staticmethod
    def get_by_id(db: Session, category_id: int) -> Optional[Category]:
        return db.query(Category).filter(Category.id == category_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
        return db.query(Category).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, name: str) -> Category:
        db_category = Category(name=name)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
