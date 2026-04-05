from fastapi import APIRouter, Depends, HTTPException, Query, Response
from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user_symptom_daily import (
    UserSymptomDailyCreate,
    UserSymptomDailyResponse,
    UserSymptomDailyUpdate
)
from app.services.user_symptom_daily_service import (
    get_user_symptom_daily_records,
    get_user_symptom_daily,
    get_user_symptom_daily_by_date,
    create_user_symptom_daily,
    update_user_symptom_daily,
    delete_user_symptom_daily
)
from app.db.session import get_db

router = APIRouter(prefix="/user-symptoms/{us_id}/daily", tags=["UserSymptomDaily"])


# 🔹 LIST
@router.get("/", response_model=List[UserSymptomDailyResponse])
def list_daily(
    us_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    data = get_user_symptom_daily_records(db, us_id, current_user.id, skip, limit)
    if data is None:
        raise HTTPException(404, "UserSymptom not found")
    return data


# 🔹 GET BY DATE (CLAVE)
@router.get("/by-date", response_model=Optional[UserSymptomDailyResponse])
def get_by_date(
    us_id: int,
    date: date = Query(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_user_symptom_daily_by_date(db, us_id, current_user.id, date)


# 🔹 CREATE / UPSERT
@router.post("/", response_model=UserSymptomDailyResponse)
def create(
    us_id: int,
    item: UserSymptomDailyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    record = create_user_symptom_daily(
        db,
        us_id,
        current_user.id,
        item.date,
        item.severity,
        item.notes
    )
    if not record:
        raise HTTPException(404, "UserSymptom not found")
    return record


# 🔹 UPDATE
@router.patch("/{daily_id}", response_model=UserSymptomDailyResponse)
def update(
    us_id: int,
    daily_id: int,
    item: UserSymptomDailyUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    record = update_user_symptom_daily(
        db,
        daily_id,
        us_id,
        current_user.id,
        item.model_dump(exclude_unset=True)
    )
    if not record:
        raise HTTPException(404, "Daily record not found")
    return record


# 🔹 DELETE
@router.delete("/{daily_id}", status_code=204)
def delete(
    us_id: int,
    daily_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    record = delete_user_symptom_daily(db, daily_id, us_id, current_user.id)
    if not record:
        raise HTTPException(404, "Daily record not found")
    return Response(status_code=204)