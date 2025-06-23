from src.models.inventory import Inventory
from datetime import datetime

class InventoryFactory:
    @staticmethod
    def create_inventory(inventory_data, store_id):
        return Inventory(
            fruit=inventory_data.fruit,
            quantity=inventory_data.quantity,
            unit=inventory_data.unit,
            store_id=store_id,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        ) 