from fastapi import APIRouter, Depends, status, Cookie
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from src.database.database import get_db
from src.models.user import User
from src.core.security import verify_token
from src.services.inventory_service import InventoryService

# Pydantic Models
class InventoryBase(BaseModel):
    fruit: str
    quantity: int
    unit: str

class InventoryCreate(InventoryBase):
    store_id: int

class InventoryUpdate(BaseModel):
    quantity: int
    unit: str

class InventoryResponse(InventoryBase):
    id: int
    store_id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

router = APIRouter()

# Dependency to get current user (similar to other routes)
async def get_current_user(access_token: str = Cookie(None), db: Session = Depends(get_db)):
    # This logic is repeated, could be moved to a shared dependency file
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

@router.post("/inventory/", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
async def create_inventory_item(
    inventory_data: InventoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return InventoryService(db).create_inventory_item(inventory_data, current_user)

@router.get("/inventory/store/{store_id}", response_model=List[InventoryResponse])
async def list_inventory_for_store(
    store_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return InventoryService(db).list_inventory_by_store(store_id, current_user)

@router.get("/inventory/{item_id}", response_model=InventoryResponse)
async def get_inventory_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return InventoryService(db).get_inventory_item(item_id, current_user)

@router.put("/inventory/{item_id}", response_model=InventoryResponse)
async def update_inventory_item(
    item_id: int,
    inventory_data: InventoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return InventoryService(db).update_inventory_item(item_id, inventory_data, current_user)

@router.delete("/inventory/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inventory_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    InventoryService(db).delete_inventory_item(item_id, current_user)
    return None 