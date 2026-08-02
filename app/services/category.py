from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.category import Category

class CategoryService:
    @staticmethod
    def create(db: Session, name: str, description: str):
        existing = db.query(Category).filter(Category.name == name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Category name already exists.")
        new_cat = Category(name=name, description=description)
        db.add(new_cat)
        db.commit()
        db.refresh(new_cat)
        return new_cat

    @staticmethod
    def get_all(db: Session):
        return db.query(Category).all()

    @staticmethod
    def get_by_id(db: Session, id: int):
        category = db.query(Category).filter(Category.id == id).first()
        if not category:
            raise HTTPException(status_code=404, detail=f"Category record matching ID {id} does not exist.")
        return category

    @staticmethod
    def update(db: Session, id: int, name: str, description: str):
        category = db.query(Category).filter(Category.id == id).first()
        if not category:
            raise HTTPException(status_code=404, detail=f"Category record matching ID {id} does not exist.")
        category.name = name
        category.description = description
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def delete(db: Session, id: int):
        category = db.query(Category).filter(Category.id == id).first()
        if not category:
            raise HTTPException(status_code=404, detail=f"Category record matching ID {id} does not exist.")
        db.delete(category)
        db.commit()
        return None
