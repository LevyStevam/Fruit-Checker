from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from src.database.database import get_db
from src.models.store import Store
from src.models.user import User
from src.core.security import verify_token
from fastapi import Cookie
from pydantic import BaseModel
from src.services.store_service import StoreService

class StoreResponse(BaseModel):
    id: int
    name: str
    cnpj: str
    employees: int
    address: str
    phone: Optional[str] = None
    email: Optional[str] = None
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

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

# Criar uma nova loja
@router.post("/stores/", status_code=status.HTTP_201_CREATED)
async def create_store(
    store_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return StoreService(db).create_store(store_data, current_user)

# Listar todas as lojas do usuário
@router.get("/stores/", response_model=List[StoreResponse])
async def list_stores(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return StoreService(db).list_stores(current_user)

# Obter uma loja específica
@router.get("/stores/{store_id}", response_model=StoreResponse)
async def get_store(
    store_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return StoreService(db).get_store(store_id, current_user)

# Atualizar uma loja
@router.put("/stores/{store_id}", response_model=StoreResponse)
async def update_store(
    store_id: int,
    store_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return StoreService(db).update_store(store_id, store_data, current_user)

# Deletar uma loja
@router.delete("/stores/{store_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_store(
    store_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    StoreService(db).delete_store(store_id, current_user)
    return None 