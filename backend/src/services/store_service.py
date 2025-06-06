from fastapi import HTTPException, status
from src.models.store import Store
from datetime import datetime
from src.models.store_factory import StoreFactory

class StoreService:
    def __init__(self, db):
        self.db = db

    def create_store(self, store_data, current_user):
        existing_store = self.db.query(Store).filter(Store.cnpj == store_data["cnpj"]).first()
        if existing_store:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CNPJ já cadastrado"
            )
        new_store = StoreFactory.create_store(store_data, current_user.id)
        self.db.add(new_store)
        self.db.commit()
        self.db.refresh(new_store)
        return new_store

    def list_stores(self, current_user):
        return self.db.query(Store).filter(Store.user_id == current_user.id).all()

    def get_store(self, store_id, current_user):
        store = self.db.query(Store).filter(
            Store.id == store_id,
            Store.user_id == current_user.id
        ).first()
        if not store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Loja não encontrada"
            )
        return store

    def update_store(self, store_id, store_data, current_user):
        store = self.db.query(Store).filter(
            Store.id == store_id,
            Store.user_id == current_user.id
        ).first()
        if not store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Loja não encontrada"
            )
        if "cnpj" in store_data and store_data["cnpj"] != store.cnpj:
            existing_store = self.db.query(Store).filter(Store.cnpj == store_data["cnpj"]).first()
            if existing_store:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="CNPJ já cadastrado"
                )
        for key, value in store_data.items():
            setattr(store, key, value)
        store.updated_at = datetime.now().isoformat()
        self.db.commit()
        self.db.refresh(store)
        return store

    def delete_store(self, store_id, current_user):
        store = self.db.query(Store).filter(
            Store.id == store_id,
            Store.user_id == current_user.id
        ).first()
        if not store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Loja não encontrada"
            )
        self.db.delete(store)
        self.db.commit() 