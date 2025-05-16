from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database import Base
from src.models.sale import Sale

class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cnpj = Column(String, unique=True, nullable=False)
    employees = Column(Integer, default=0)
    address = Column(String, nullable=False)
    phone = Column(String)
    email = Column(String)
    created_at = Column(String)  # Data de criação da loja
    updated_at = Column(String)  # Data da última atualização
    
    # Relacionamento com o usuário (dono da loja)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="stores")
    # Relacionamento com vendas
    sales = relationship("Sale", back_populates="store") 