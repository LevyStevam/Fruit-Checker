from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database import Base
from src.models.base_entity import BaseEntity

class Sale(BaseEntity, Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    fruit = Column(String, nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    store = relationship("Store", back_populates="sales") 