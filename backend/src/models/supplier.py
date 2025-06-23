from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from src.database.database import Base
from src.models.base_entity import BaseEntity

class Supplier(BaseEntity, Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cnpj = Column(String, nullable=False)
    address = Column(String, nullable=False)
    fruits = Column(Text)  # Storing fruits as a simple text field, e.g., "Maçã, Banana, Laranja"
    
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    store = relationship("Store", back_populates="suppliers") 