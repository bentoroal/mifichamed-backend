from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.schemas.user_symptom import UserSymptomCreate, UserSymptomResponse
from app.services.user_symptom_service import get_user_symptoms, get_user_symptom, create_user_symptom, delete_user_symptom
from app.db.session import get_db

router = APIRouter(prefix="/user-symptoms", tags=["UserSymptoms"])


@router.get("/", response_model=List[UserSymptomResponse])
def list_user_symptoms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_user_symptoms(db, skip, limit)


@router.post("/", response_model=UserSymptomResponse)
def create(item: UserSymptomCreate, db: Session = Depends(get_db)):
    return create_user_symptom(db, item.user_id, item.symptom_id, item.start_date, item.severity, item.is_current, item.notes, item.linked_condition_id)


@router.get("/{us_id}", response_model=UserSymptomResponse)
def read(us_id: int, db: Session = Depends(get_db)):
    db_obj = get_user_symptom(db, us_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="UserSymptom not found")
    return db_obj


@router.delete("/{us_id}", response_model=UserSymptomResponse)
def remove(us_id: int, db: Session = Depends(get_db)):
    obj = delete_user_symptom(db, us_id)
    if not obj:
        raise HTTPException(status_code=404, detail="UserSymptom not found")
    return obj
