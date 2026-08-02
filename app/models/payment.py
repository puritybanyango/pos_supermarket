import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    payment_method = Column(String, nullable=False)  # CASH, CARD, MOBILE
    amount_paid = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)

    sale = relationship("Sale", back_populates="payments")
