from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database import Base
from src.models.base_entity import BaseEntity

class Inventory(BaseEntity, Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    fruit = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit = Column(String, nullable=False)  # e.g., 'kg', 'units'
    
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    store = relationship("Store", back_populates="inventory") 