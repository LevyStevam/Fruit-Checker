from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database import Base
from src.models.sale import Sale
from src.models.base_entity import BaseEntity
from src.models.inventory import Inventory

class Store(BaseEntity, Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    _name = Column("name", String, nullable=False)
    _cnpj = Column("cnpj", String, unique=True, nullable=False)
    _employees = Column("employees", Integer, default=0)
    _address = Column("address", String, nullable=False)
    _phone = Column("phone", String)
    _email = Column("email", String)
    # created_at e updated_at agora vêm da BaseEntity
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="stores")
    sales = relationship("Sale", back_populates="store")
    inventory = relationship("Inventory", back_populates="store")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def cnpj(self):
        return self._cnpj

    @cnpj.setter
    def cnpj(self, value):
        self._cnpj = value

    @property
    def employees(self):
        return self._employees

    @employees.setter
    def employees(self, value):
        self._employees = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self._phone = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value 