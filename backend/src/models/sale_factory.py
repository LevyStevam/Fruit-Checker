from src.models.sale import Sale
from datetime import datetime

class SaleFactory:
    @staticmethod
    def create_sale(sale_data, store_id):
        return Sale(
            value=sale_data.value,
            quantity=sale_data.quantity,
            fruit=sale_data.fruit,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            store_id=store_id
        ) 