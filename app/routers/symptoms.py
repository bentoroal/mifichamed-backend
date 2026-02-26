from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.symptom import SymptomCatalogCreate, SymptomCatalogResponse
from app.services.symptom_service import get_symptoms, get_symptom, create_symptom, delete_symptom
from app.db.session import get_db

router = APIRouter(prefix="/symptoms", tags=["Symptoms"])


@router.get("/", response_model=List[SymptomCatalogResponse])
def list_symptoms(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_symptoms(db, current_user.id, skip, limit)


@router.post("/", response_model=SymptomCatalogResponse)
def create(
    item: SymptomCatalogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # ignore any user id provided, always use auth user
    return create_symptom(db, item.name, current_user.id, item.is_custom)


@router.get("/{symptom_id}", response_model=SymptomCatalogResponse)
def read(
    symptom_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_obj = get_symptom(db, symptom_id, current_user.id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Symptom not found")
    return db_obj


@router.delete("/{symptom_id}", response_model=SymptomCatalogResponse)
def remove(
    symptom_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    obj = delete_symptom(db, symptom_id, current_user.id)
    if not obj:
        raise HTTPException(status_code=404, detail="Symptom not found or not owned")
    return obj
