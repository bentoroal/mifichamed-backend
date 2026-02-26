from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.condition import ConditionCatalogCreate, ConditionCatalogResponse
from app.services.condition_service import get_conditions, get_condition, create_condition, delete_condition
from app.db.session import get_db

router = APIRouter(prefix="/conditions", tags=["Conditions"])


@router.get("/", response_model=List[ConditionCatalogResponse])
def list_conditions(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_conditions(db, current_user.id, skip, limit)


@router.post("/", response_model=ConditionCatalogResponse)
def create(
    cond: ConditionCatalogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_condition(db, cond.name, current_user.id, cond.is_custom)


@router.get("/{condition_id}", response_model=ConditionCatalogResponse)
def read(
    condition_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_obj = get_condition(db, condition_id, current_user.id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Condition not found")
    return db_obj


@router.delete("/{condition_id}", response_model=ConditionCatalogResponse)
def remove(
    condition_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    obj = delete_condition(db, condition_id, current_user.id)
    if not obj:
        raise HTTPException(status_code=404, detail="Condition not found or not owned")
    return obj
