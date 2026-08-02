from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from app.models.category import Category
from app.services.category import CategoryService
from app.schemas import CategoryCreate, CategoryResponse
router = APIRouter(prefix="/categories", tags=["Category"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_category(name: str, description: str, db: Session = Depends(get_db)):
    existing = db.query(Category).filter(Category.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category name already exists.")
    new_cat = Category(name=name, description=description)
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return new_cat

@router.get("/")
def get_all_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.get("/{id}")
def get_category_by_id(id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail=f"Category record matching ID {id} does not exist.")
    return category

@router.put("/{id}")
def update_category(id: int, name: str, description: str, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail=f"Category record matching ID {id} does not exist.")
    category.name = name
    category.description = description
    db.commit()
    db.refresh(category)
    return category

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail=f"Category record matching ID {id} does not exist.")
    db.delete(category)
    db.commit()
    return None



from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from app.services.category import CategoryService


