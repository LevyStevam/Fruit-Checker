from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from src.database.database import get_db
from src.models.sale import Sale
from src.models.store import Store
from src.models.user import User
from src.core.security import verify_token
from fastapi import Cookie
from pydantic import BaseModel

class SaleResponse(BaseModel):
    id: int
    value: float
    quantity: int
    fruit: str
    created_at: str
    store_id: int

    class Config:
        from_attributes = True

class SaleCreate(BaseModel):
    value: float
    quantity: int
    fruit: str
    store_id: int

router = APIRouter()

# Função para obter o usuário atual
async def get_current_user(access_token: str = Cookie(None), db: Session = Depends(get_db)):
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado"
        )
    try:
        payload = verify_token(access_token)
        user = db.query(User).filter(User.email == payload["sub"]).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não encontrado"
            )
        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

# Criar uma nova venda
@router.post("/sales/", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
async def create_sale(
    sale_data: SaleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verificar se a loja existe e pertence ao usuário
    store = db.query(Store).filter(Store.id == sale_data.store_id, Store.user_id == current_user.id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Loja não encontrada")
    new_sale = Sale(
        value=sale_data.value,
        quantity=sale_data.quantity,
        fruit=sale_data.fruit,
        created_at=datetime.now().isoformat(),
        store_id=sale_data.store_id
    )
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)
    return new_sale

# Listar todas as vendas do usuário
@router.get("/sales/", response_model=List[SaleResponse])
async def list_sales(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Buscar todas as vendas das lojas do usuário
    stores = db.query(Store).filter(Store.user_id == current_user.id).all()
    store_ids = [store.id for store in stores]
    sales = db.query(Sale).filter(Sale.store_id.in_(store_ids)).all()
    return sales

# Obter uma venda específica
@router.get("/sales/{sale_id}", response_model=SaleResponse)
async def get_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sale = db.query(Sale).join(Store).filter(
        Sale.id == sale_id,
        Store.user_id == current_user.id
    ).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return sale

# Atualizar uma venda
@router.put("/sales/{sale_id}", response_model=SaleResponse)
async def update_sale(
    sale_id: int,
    sale_data: SaleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sale = db.query(Sale).join(Store).filter(
        Sale.id == sale_id,
        Store.user_id == current_user.id
    ).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    # Verificar se a loja existe e pertence ao usuário
    store = db.query(Store).filter(Store.id == sale_data.store_id, Store.user_id == current_user.id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Loja não encontrada")
    sale.value = sale_data.value
    sale.quantity = sale_data.quantity
    sale.fruit = sale_data.fruit
    sale.store_id = sale_data.store_id
    db.commit()
    db.refresh(sale)
    return sale

# Deletar uma venda
@router.delete("/sales/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sale = db.query(Sale).join(Store).filter(
        Sale.id == sale_id,
        Store.user_id == current_user.id
    ).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    db.delete(sale)
    db.commit()
    return None 