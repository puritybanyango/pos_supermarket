from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from app.services.user import UserService
from app.schemas import UserCreate, UserResponse
from typing import List

router = APIRouter(prefix="/users", tags=["User"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    """Registers a new supermarket system operator account."""
    return UserService.create(db, payload.username, payload.role)

@router.get("/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """Retrieves a list of all supermarket system user accounts."""
    return UserService.get_all(db)

@router.get("/{id}", response_model=UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    """Retrieves a single system user account using its ID."""
    return UserService.get_by_id(db, id)

@router.put("/{id}", response_model=UserResponse)
def update_user_profile(id: int, role: str, is_active: bool, db: Session = Depends(get_db)):
    """Updates an employee's system permissions role or access status using their ID."""
    return UserService.update(db, id, role, is_active)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    """Permanently deletes a system user account record from the database using its ID."""
    return UserService.delete(db, id)

