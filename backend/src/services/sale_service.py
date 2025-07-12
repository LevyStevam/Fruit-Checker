from fastapi import HTTPException, status
from src.models.sale import Sale
from src.models.store import Store
from datetime import datetime
from src.models.sale_factory import SaleFactory
from src.models.user import User
from src.models.inventory import Inventory
from src.core.email_utils import send_email_notification

class SaleService:
    def __init__(self, db):
        self.db = db

    def create_sale(self, sale_data, current_user):
        store = self.db.query(Store).filter(Store.id == sale_data.store_id, Store.user_id == current_user.id).first()
        if not store:
            raise HTTPException(status_code=404, detail="Loja não encontrada")
        # Buscar item de estoque
        inventory_item = self.db.query(Inventory).filter(
            Inventory.store_id == sale_data.store_id,
            Inventory.fruit == sale_data.fruit
        ).first()
        if not inventory_item:
            raise HTTPException(status_code=404, detail="Fruta não encontrada no estoque da loja")
        if inventory_item.quantity < sale_data.quantity:
            raise HTTPException(status_code=400, detail=f"Estoque insuficiente para a fruta '{sale_data.fruit}'. Quantidade disponível: {inventory_item.quantity}")
        # Descontar do estoque
        inventory_item.quantity -= sale_data.quantity
        inventory_item.updated_at = datetime.now().isoformat()
        self.db.commit()
        # Buscar e-mail do usuário dono da loja
        user = self.db.query(User).filter(User.id == store.user_id).first()
        user_email = user.email if user else None
        # Criar venda
        new_sale = SaleFactory.create_sale(sale_data, sale_data.store_id)
        self.db.add(new_sale)
        self.db.commit()
        self.db.refresh(new_sale)
        # Enviar notificação por e-mail
        if user_email:
            try:
                send_email_notification(
                    to_email=user_email,
                    subject=f"Nova venda realizada - {sale_data.fruit}",
                    body=f"Uma nova venda foi realizada na loja '{store.name}'.\nFruta: {sale_data.fruit}\nQuantidade: {sale_data.quantity}\nValor: R$ {sale_data.value:.2f}"
                )
            except Exception as e:
                print(f"Erro ao enviar e-mail de notificação de venda: {e}")
        # Notificação de estoque baixo
        if inventory_item.quantity < 20 and user_email:
            try:
                send_email_notification(
                    to_email=user_email,
                    subject=f"Estoque baixo: {sale_data.fruit}",
                    body=f"O estoque da fruta '{sale_data.fruit}' na loja '{store.name}' está abaixo de 20 unidades. Quantidade atual: {inventory_item.quantity}."
                )
            except Exception as e:
                print(f"Erro ao enviar e-mail de notificação de estoque baixo: {e}")
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