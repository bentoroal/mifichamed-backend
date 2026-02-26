from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user_condition import UserConditionCreate, UserConditionResponse
from app.services.user_condition_service import (
    get_user_conditions,
    get_user_condition,
    create_user_condition,
    delete_user_condition,
)
from app.db.session import get_db

router = APIRouter(prefix="/user-conditions", tags=["UserConditions"])


@router.get("/", response_model=List[UserConditionResponse])
def list_user_conditions(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_user_conditions(db, current_user.id, skip, limit)


@router.post("/", response_model=UserConditionResponse)
def create(
    item: UserConditionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # ignore user_id from request, always use authenticated user
    return create_user_condition(
        db,
        current_user.id,
        item.condition_id,
        item.diagnosis_date,
        item.status,
        item.notes,
    )


@router.get("/{uc_id}", response_model=UserConditionResponse)
def read(
    uc_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_obj = get_user_condition(db, uc_id, current_user.id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="UserCondition not found")
    return db_obj


@router.delete("/{uc_id}", response_model=UserConditionResponse)
def remove(
    uc_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    obj = delete_user_condition(db, uc_id, current_user.id)
    if not obj:
        raise HTTPException(status_code=404, detail="UserCondition not found")
    return obj
