from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user_symptom import UserSymptomCreate, UserSymptomResponse, UserSymptomUpdate
from app.schemas.user_symptom_daily import UserSymptomDailyCreate, UserSymptomDailyResponse, UserSymptomDailyUpdate
from app.services.user_symptom_service import get_user_symptoms, get_user_symptom, create_user_symptom, delete_user_symptom, update_user_symptom
from app.services.user_symptom_daily_service import (
    get_user_symptom_daily_records,
    get_user_symptom_daily,
    create_user_symptom_daily,
    update_user_symptom_daily,
    delete_user_symptom_daily
)
from app.db.session import get_db

router = APIRouter(prefix="/user-symptoms", tags=["UserSymptoms"])

# --------------------------------------------------
# collection endpoints
# --------------------------------------------------

@router.get("/", response_model=List[UserSymptomResponse])
def list_user_symptoms(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_user_symptoms(db, current_user.id, skip, limit)


@router.get("/{us_id}", response_model=UserSymptomResponse)
def read(
    us_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_obj = get_user_symptom(db, us_id, current_user.id)

    if not db_obj:
        raise HTTPException(status_code=404, detail="UserSymptom not found")

    return db_obj


@router.post("/", response_model=UserSymptomResponse)
def create(
    item: UserSymptomCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
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


@router.delete("/{us_id}", response_model=UserSymptomResponse)
def remove(
    us_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    # only allow deleting symptoms belonging to the signed‑in user
    dbobj = delete_user_symptom(
        db,
        us_id,
        current_user.id
    )
    if not dbobj:
        raise HTTPException(status_code=404, detail="UserSymptom not found")
    return dbobj

@router.patch("/{us_id}", response_model=UserSymptomResponse)
def update(
    us_id: int,
    item: UserSymptomUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    db_obj = update_user_symptom(
        db,
        us_id,
        current_user.id,
        item.model_dump(exclude_unset=True)
    )

    if not db_obj:
        raise HTTPException(status_code=404, detail="UserSymptom not found")

    return db_obj


# --------------------------------------------------
# daily records endpoints
# --------------------------------------------------

@router.post("/{us_id}/daily", response_model=UserSymptomDailyResponse)
def create_daily_record(
    us_id: int,
    item: UserSymptomDailyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crear un registro diario de intensidad del síntoma"""
    daily_record = create_user_symptom_daily(
        db,
        us_id,
        current_user.id,
        item.date,
        item.severity,
        item.notes
    )
    
    if not daily_record:
        raise HTTPException(status_code=404, detail="UserSymptom not found")
    
    return daily_record


@router.get("/{us_id}/daily", response_model=List[UserSymptomDailyResponse])
def list_daily_records(
    us_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Listar todos los registros diarios de un síntoma"""
    daily_records = get_user_symptom_daily_records(db, us_id, current_user.id, skip, limit)
    
    if daily_records is None:
        raise HTTPException(status_code=404, detail="UserSymptom not found")
    
    return daily_records


@router.get("/{us_id}/daily/{daily_id}", response_model=UserSymptomDailyResponse)
def read_daily_record(
    us_id: int,
    daily_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener un registro diario específico"""
    daily_record = get_user_symptom_daily(db, daily_id, us_id, current_user.id)
    
    if not daily_record:
        raise HTTPException(status_code=404, detail="Daily record not found")
    
    return daily_record


@router.patch("/{us_id}/daily/{daily_id}", response_model=UserSymptomDailyResponse)
def update_daily_record(
    us_id: int,
    daily_id: int,
    item: UserSymptomDailyUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Actualizar un registro diario"""
    daily_record = update_user_symptom_daily(
        db,
        daily_id,
        us_id,
        current_user.id,
        item.model_dump(exclude_unset=True)
    )
    
    if not daily_record:
        raise HTTPException(status_code=404, detail="Daily record not found")
    
    return daily_record


@router.delete("/{us_id}/daily/{daily_id}", response_model=UserSymptomDailyResponse)
def delete_daily_record(
    us_id: int,
    daily_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Eliminar un registro diario"""
    daily_record = delete_user_symptom_daily(db, daily_id, us_id, current_user.id)
    
    if not daily_record:
        raise HTTPException(status_code=404, detail="Daily record not found")
    
    return daily_record
