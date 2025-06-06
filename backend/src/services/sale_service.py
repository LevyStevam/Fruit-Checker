from fastapi import HTTPException, status
from src.models.sale import Sale
from src.models.store import Store
from datetime import datetime
from src.models.sale_factory import SaleFactory

class SaleService:
    def __init__(self, db):
        self.db = db

    def create_sale(self, sale_data, current_user):
        store = self.db.query(Store).filter(Store.id == sale_data.store_id, Store.user_id == current_user.id).first()
        if not store:
            raise HTTPException(status_code=404, detail="Loja não encontrada")
        new_sale = SaleFactory.create_sale(sale_data, sale_data.store_id)
        self.db.add(new_sale)
        self.db.commit()
        self.db.refresh(new_sale)
        return new_sale

    def list_sales(self, current_user):
        stores = self.db.query(Store).filter(Store.user_id == current_user.id).all()
        store_ids = [store.id for store in stores]
        sales = self.db.query(Sale).filter(Sale.store_id.in_(store_ids)).all()
        return sales

    def get_sale(self, sale_id, current_user):
        sale = self.db.query(Sale).join(Store).filter(
            Sale.id == sale_id,
            Store.user_id == current_user.id
        ).first()
        if not sale:
            raise HTTPException(status_code=404, detail="Venda não encontrada")
        return sale

    def update_sale(self, sale_id, sale_data, current_user):
        sale = self.db.query(Sale).join(Store).filter(
            Sale.id == sale_id,
            Store.user_id == current_user.id
        ).first()
        if not sale:
            raise HTTPException(status_code=404, detail="Venda não encontrada")
        store = self.db.query(Store).filter(Store.id == sale_data.store_id, Store.user_id == current_user.id).first()
        if not store:
            raise HTTPException(status_code=404, detail="Loja não encontrada")
        sale.value = sale_data.value
        sale.quantity = sale_data.quantity
        sale.fruit = sale_data.fruit
        sale.store_id = sale_data.store_id
        sale.updated_at = datetime.now().isoformat()
        self.db.commit()
        self.db.refresh(sale)
        return sale

    def delete_sale(self, sale_id, current_user):
        sale = self.db.query(Sale).join(Store).filter(
            Sale.id == sale_id,
            Store.user_id == current_user.id
        ).first()
        if not sale:
            raise HTTPException(status_code=404, detail="Venda não encontrada")
        self.db.delete(sale)
        self.db.commit() 