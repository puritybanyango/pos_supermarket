import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    receipt_number = Column(String, unique=True, index=True, nullable=False) # e.g., REC-2026-0001
    issued_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)

    sale = relationship("Sale", back_populates="receipts")
