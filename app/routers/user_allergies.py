from fastapi import APIRouter, Depends, HTTPException, Response
from typing import List
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.allergy import (
    UserAllergyCreate,
    UserAllergyResponse,
    UserAllergyUpdate,
)
from app.services.user_allergy_service import (
    get_user_allergies,
    get_user_allergy,
    create_user_allergy,
    delete_user_allergy,
    update_user_allergy,
)
from app.db.session import get_db

router = APIRouter(prefix="/user-allergies", tags=["UserAllergies"])


@router.get("/", response_model=List[UserAllergyResponse])
def list_user_allergies(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_user_allergies(db, current_user.id, skip, limit)


@router.get("/{ua_id}", response_model=UserAllergyResponse)
def read(
    ua_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_obj = get_user_allergy(db, ua_id, current_user.id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="UserAllergy not found")
    return db_obj


@router.post("/", response_model=UserAllergyResponse)
def create(
    item: UserAllergyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_user_allergy(
        db,
        current_user.id,
        allergy_id=getattr(item, "allergy_id", None),
        name=getattr(item, "name", None),
        status=item.status,
        start_date=item.start_date,
        end_date=item.end_date,
        notes=item.notes,
    )


@router.delete("/{ua_id}", response_model=UserAllergyResponse)
def remove(
    ua_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    obj = delete_user_allergy(db, ua_id, current_user.id)
    if not obj:
        raise HTTPException(status_code=404, detail="UserAllergy not found")
    return Response(status_code=204)


@router.patch("/{ua_id}", response_model=UserAllergyResponse)
def update(
    ua_id: int,
    item: UserAllergyUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_obj = update_user_allergy(
        db,
        ua_id,
        current_user.id,
        item.model_dump(exclude_unset=True),
    )
    if not db_obj:
        raise HTTPException(status_code=404, detail="UserAllergy not found")
    return db_obj
