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
    # Verificar se o CNPJ já existe
    existing_store = db.query(Store).filter(Store.cnpj == store_data["cnpj"]).first()
    if existing_store:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CNPJ já cadastrado"
        )
    
    # Criar nova loja
    new_store = Store(
        **store_data,
        user_id=current_user.id,
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )
    
    db.add(new_store)
    db.commit()
    db.refresh(new_store)
    return new_store

# Listar todas as lojas do usuário
@router.get("/stores/", response_model=List[StoreResponse])
async def list_stores(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stores = db.query(Store).filter(Store.user_id == current_user.id).all()
    return stores

# Obter uma loja específica
@router.get("/stores/{store_id}", response_model=StoreResponse)
async def get_store(
    store_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    store = db.query(Store).filter(
        Store.id == store_id,
        Store.user_id == current_user.id
    ).first()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loja não encontrada"
        )
    
    return store

# Atualizar uma loja
@router.put("/stores/{store_id}", response_model=StoreResponse)
async def update_store(
    store_id: int,
    store_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    store = db.query(Store).filter(
        Store.id == store_id,
        Store.user_id == current_user.id
    ).first()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loja não encontrada"
        )
    
    # Verificar se o novo CNPJ já existe (se estiver sendo alterado)
    if "cnpj" in store_data and store_data["cnpj"] != store.cnpj:
        existing_store = db.query(Store).filter(Store.cnpj == store_data["cnpj"]).first()
        if existing_store:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CNPJ já cadastrado"
            )
    
    # Atualizar os campos
    for key, value in store_data.items():
        setattr(store, key, value)
    
    store.updated_at = datetime.now().isoformat()
    
    db.commit()
    db.refresh(store)
    return store

# Deletar uma loja
@router.delete("/stores/{store_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_store(
    store_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    store = db.query(Store).filter(
        Store.id == store_id,
        Store.user_id == current_user.id
    ).first()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loja não encontrada"
        )
    
    db.delete(store)
    db.commit()
    return None 