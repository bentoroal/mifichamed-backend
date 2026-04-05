from fastapi import APIRouter, Depends, HTTPException, Response
from typing import List
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user_symptom import UserSymptomCreate, UserSymptomResponse, UserSymptomUpdate
from app.services.user_symptom_service import (
    get_user_symptoms,
    get_user_symptom,
    create_user_symptom,
    delete_user_symptom,
    update_user_symptom
)
from app.db.session import get_db

router = APIRouter(prefix="/user-symptoms", tags=["UserSymptoms"])


@router.get("/", response_model=List[UserSymptomResponse])
def list_user_symptoms(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_user_symptoms(db, current_user.id, skip, limit)


@router.get("/{us_id}", response_model=UserSymptomResponse)
def read(us_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    obj = get_user_symptom(db, us_id, current_user.id)
    if not obj:
        raise HTTPException(404, "UserSymptom not found")
    return obj


@router.post("/", response_model=UserSymptomResponse)
def create(item: UserSymptomCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return create_user_symptom(
        db,
        current_user.id,
        item.symptom_id,
        item.start_date,
        item.end_date,
        item.severity,
        item.is_current,
        item.notes
    )


@router.patch("/{us_id}", response_model=UserSymptomResponse)
def update(us_id: int, item: UserSymptomUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    obj = update_user_symptom(
        db,
        us_id,
        current_user.id,
        item.model_dump(exclude_unset=True)
    )
    if not obj:
        raise HTTPException(404, "UserSymptom not found")
    return obj


@router.delete("/{us_id}", response_model=UserSymptomResponse)
def remove(us_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    obj = delete_user_symptom(db, us_id, current_user.id)
    if not obj:
        raise HTTPException(404, "UserSymptom not found")
    return Response(status_code=204)