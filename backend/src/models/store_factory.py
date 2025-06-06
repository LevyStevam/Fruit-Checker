from src.models.store import Store
from datetime import datetime

class StoreFactory:
    @staticmethod
    def create_store(store_data, user_id):
        return Store(
            **store_data,
            user_id=user_id,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        ) 