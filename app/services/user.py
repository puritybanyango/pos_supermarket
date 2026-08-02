from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User

class UserService:
    def create(db: Session, username: str, role: str):
        if db.query(User).filter(User.username == username).first():
            raise HTTPException(status_code=400, detail="Username already in use.")
        new_user = User(username=username, hashed_password="DELEGATED_PASSWORD_STUB", role=role, is_active=True)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def get_all(db: Session):
        return db.query(User).all()

    def get_by_id(db: Session, id: int):
        user = db.query(User).filter(User.id == id).first()
        if not user:
            raise HTTPException(status_code=404, detail=f"User record matching ID {id} does not exist.")
        return user

    def update(db: Session, id: int, role: str, is_active: bool):
        user = db.query(User).filter(User.id == id).first()
        if not user:
            raise HTTPException(status_code=404, detail=f"User record matching ID {id} does not exist.")
        
        user.role = role
        user.is_active = is_active
        db.commit()
        db.refresh(user)
        return user

    def delete(db: Session, id: int):
        user = db.query(User).filter(User.id == id).first()
        if not user:
            raise HTTPException(status_code=404, detail=f"User record matching ID {id} does not exist.")
        db.delete(user)
        db.commit()
        return None
