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
from src.services.sale_service import SaleService

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
    return SaleService(db).create_sale(sale_data, current_user)

# Listar todas as vendas do usuário
@router.get("/sales/", response_model=List[SaleResponse])
async def list_sales(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return SaleService(db).list_sales(current_user)

# Obter uma venda específica
@router.get("/sales/{sale_id}", response_model=SaleResponse)
async def get_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return SaleService(db).get_sale(sale_id, current_user)

# Atualizar uma venda
@router.put("/sales/{sale_id}", response_model=SaleResponse)
async def update_sale(
    sale_id: int,
    sale_data: SaleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return SaleService(db).update_sale(sale_id, sale_data, current_user)

# Deletar uma venda
@router.delete("/sales/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    SaleService(db).delete_sale(sale_id, current_user)
    return None 