from fastapi import HTTPException, status
from src.models.inventory import Inventory
from src.models.store import Store
from src.models.inventory_factory import InventoryFactory
from datetime import datetime

class InventoryService:
    def __init__(self, db):
        self.db = db

    def create_inventory_item(self, inventory_data, current_user):
        store = self.db.query(Store).filter(Store.id == inventory_data.store_id, Store.user_id == current_user.id).first()
        if not store:
            raise HTTPException(status_code=404, detail="Loja não encontrada")
        
        # Check if fruit already exists in this store's inventory
        existing_item = self.db.query(Inventory).filter(Inventory.store_id == inventory_data.store_id, Inventory.fruit == inventory_data.fruit).first()
        if existing_item:
            raise HTTPException(status_code=400, detail="Fruta já existe no inventário desta loja")

        new_item = InventoryFactory.create_inventory(inventory_data, inventory_data.store_id)
        self.db.add(new_item)
        self.db.commit()
        self.db.refresh(new_item)
        return new_item

    def list_inventory_by_store(self, store_id, current_user):
        store = self.db.query(Store).filter(Store.id == store_id, Store.user_id == current_user.id).first()
        if not store:
            raise HTTPException(status_code=404, detail="Loja não encontrada")
        return self.db.query(Inventory).filter(Inventory.store_id == store_id).all()

    def get_inventory_item(self, item_id, current_user):
        item = self.db.query(Inventory).join(Store).filter(
            Inventory.id == item_id,
            Store.user_id == current_user.id
        ).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item do inventário não encontrado")
        return item

    def update_inventory_item(self, item_id, inventory_data, current_user):
        item = self.get_inventory_item(item_id, current_user) # Re-uses the get method to ensure ownership
        
        item.quantity = inventory_data.quantity
        item.unit = inventory_data.unit
        item.updated_at = datetime.now().isoformat()
        
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete_inventory_item(self, item_id, current_user):
        item = self.get_inventory_item(item_id, current_user) # Re-uses the get method to ensure ownership
        self.db.delete(item)
        self.db.commit() 