from fastapi import HTTPException, status
from src.models.supplier import Supplier
from src.models.store import Store
from src.models.supplier_factory import SupplierFactory
from datetime import datetime

class SupplierService:
    def __init__(self, db):
        self.db = db

    def create_supplier(self, supplier_data, current_user):
        store = self.db.query(Store).filter(Store.id == supplier_data.store_id, Store.user_id == current_user.id).first()
        if not store:
            raise HTTPException(status_code=404, detail="Loja não encontrada")

        existing_supplier = self.db.query(Supplier).filter(Supplier.store_id == supplier_data.store_id, Supplier.cnpj == supplier_data.cnpj).first()
        if existing_supplier:
            raise HTTPException(status_code=400, detail="CNPJ do fornecedor já cadastrado para esta loja")

        new_supplier = SupplierFactory.create_supplier(supplier_data, supplier_data.store_id)
        self.db.add(new_supplier)
        self.db.commit()
        self.db.refresh(new_supplier)
        return new_supplier

    def list_suppliers_by_store(self, store_id, current_user):
        store = self.db.query(Store).filter(Store.id == store_id, Store.user_id == current_user.id).first()
        if not store:
            raise HTTPException(status_code=404, detail="Loja não encontrada")
        return self.db.query(Supplier).filter(Supplier.store_id == store_id).all()

    def get_supplier(self, supplier_id, current_user):
        supplier = self.db.query(Supplier).join(Store).filter(
            Supplier.id == supplier_id,
            Store.user_id == current_user.id
        ).first()
        if not supplier:
            raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
        return supplier

    def update_supplier(self, supplier_id, supplier_data, current_user):
        supplier = self.get_supplier(supplier_id, current_user)
        
        # Check for CNPJ conflict if it's being changed
        if supplier_data.cnpj != supplier.cnpj:
            existing_supplier = self.db.query(Supplier).filter(Supplier.store_id == supplier.store_id, Supplier.cnpj == supplier_data.cnpj).first()
            if existing_supplier:
                raise HTTPException(status_code=400, detail="CNPJ do fornecedor já cadastrado para esta loja")

        supplier.name = supplier_data.name
        supplier.cnpj = supplier_data.cnpj
        supplier.address = supplier_data.address
        supplier.fruits = supplier_data.fruits
        supplier.updated_at = datetime.now().isoformat()
        
        self.db.commit()
        self.db.refresh(supplier)
        return supplier

    def delete_supplier(self, supplier_id, current_user):
        supplier = self.get_supplier(supplier_id, current_user)
        self.db.delete(supplier)
        self.db.commit() 