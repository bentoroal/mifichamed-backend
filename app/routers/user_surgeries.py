from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.surgery import (
    UserSurgeryCreate,
    UserSurgeryResponse,
    UserSurgeryUpdate,
)
from app.services.user_surgery_service import (
    get_user_surgeries,
    get_user_surgery,
    create_user_surgery,
    delete_user_surgery,
    update_user_surgery,
)
from app.db.session import get_db

router = APIRouter(prefix="/user-surgeries", tags=["UserSurgeries"])


@router.get("/", response_model=List[UserSurgeryResponse])
def list_user_surgeries(
    skip: int = 0,
    limit: int = 100,
    condition_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_user_surgeries(db, current_user.id, skip, limit, condition_id)


@router.get("/{us_id}", response_model=UserSurgeryResponse)
def read(
    us_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_obj = get_user_surgery(db, us_id, current_user.id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="UserSurgery not found")
    return db_obj


@router.post("/", response_model=UserSurgeryResponse)
def create(
    item: UserSurgeryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_user_surgery(
        db,
        current_user.id,
        surgery_id=getattr(item, "surgery_id", None),
        name=getattr(item, "name", None),
        user_condition_id=item.user_condition_id,
        surgery_date=item.surgery_date,
        notes=item.notes,
    )


@router.delete("/{us_id}", response_model=UserSurgeryResponse)
def remove(
    us_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    obj = delete_user_surgery(db, us_id, current_user.id)
    if not obj:
        raise HTTPException(status_code=404, detail="UserSurgery not found")
    return obj


@router.patch("/{us_id}", response_model=UserSurgeryResponse)
def update(
    us_id: int,
    item: UserSurgeryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_obj = update_user_surgery(
        db,
        us_id,
        current_user.id,
        item.model_dump(exclude_unset=True),
    )
    if not db_obj:
        raise HTTPException(status_code=404, detail="UserSurgery not found")
    return db_obj
