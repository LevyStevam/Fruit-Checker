from src.models.supplier import Supplier
from datetime import datetime

class SupplierFactory:
    @staticmethod
    def create_supplier(supplier_data, store_id):
        return Supplier(
            name=supplier_data.name,
            cnpj=supplier_data.cnpj,
            address=supplier_data.address,
            fruits=supplier_data.fruits,
            store_id=store_id,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        ) 