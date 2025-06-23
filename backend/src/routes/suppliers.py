from fastapi import APIRouter, Depends, status, Cookie
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from src.database.database import get_db
from src.models.user import User
from src.core.security import verify_token
from src.services.supplier_service import SupplierService

# Pydantic Models
class SupplierBase(BaseModel):
    name: str
    cnpj: str
    address: str
    fruits: str

class SupplierCreate(SupplierBase):
    store_id: int

class SupplierUpdate(SupplierBase):
    pass

class SupplierResponse(SupplierBase):
    id: int
    store_id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

router = APIRouter()

# Dependency to get current user
async def get_current_user(access_token: str = Cookie(None), db: Session = Depends(get_db)):
    if not access_token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Não autenticado")
    try:
        payload = verify_token(access_token)
        user = db.query(User).filter(User.email == payload["sub"]).first()
        if not user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")
        return user
    except Exception:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

@router.post("/suppliers/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
async def create_supplier(
    supplier_data: SupplierCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return SupplierService(db).create_supplier(supplier_data, current_user)

@router.get("/suppliers/store/{store_id}", response_model=List[SupplierResponse])
async def list_suppliers_for_store(
    store_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return SupplierService(db).list_suppliers_by_store(store_id, current_user)

@router.get("/suppliers/{supplier_id}", response_model=SupplierResponse)
async def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return SupplierService(db).get_supplier(supplier_id, current_user)

@router.put("/suppliers/{supplier_id}", response_model=SupplierResponse)
async def update_supplier(
    supplier_id: int,
    supplier_data: SupplierUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return SupplierService(db).update_supplier(supplier_id, supplier_data, current_user)

@router.delete("/suppliers/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    SupplierService(db).delete_supplier(supplier_id, current_user)
    return None 