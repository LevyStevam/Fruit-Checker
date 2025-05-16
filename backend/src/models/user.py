from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.database import Base
from src.models.store import Store

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    
    # Relacionamento com as lojas
    stores = relationship("Store", back_populates="user") 