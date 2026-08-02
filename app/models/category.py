from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    # Back-reference connection tracking
    products = relationship("Product", back_populates="category")
