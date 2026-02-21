from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.schemas.symptom import SymptomCatalogCreate, SymptomCatalogResponse
from app.services.symptom_service import get_symptoms, get_symptom, create_symptom, delete_symptom
from app.db.session import get_db

router = APIRouter(prefix="/symptoms", tags=["Symptoms"])


@router.get("/", response_model=List[SymptomCatalogResponse])
def list_symptoms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_symptoms(db, skip, limit)


@router.post("/", response_model=SymptomCatalogResponse)
def create(item: SymptomCatalogCreate, db: Session = Depends(get_db)):
    return create_symptom(db, item.name, item.is_custom, item.created_by_user_id)


@router.get("/{symptom_id}", response_model=SymptomCatalogResponse)
def read(symptom_id: int, db: Session = Depends(get_db)):
    db_obj = get_symptom(db, symptom_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Symptom not found")
    return db_obj


@router.delete("/{symptom_id}", response_model=SymptomCatalogResponse)
def remove(symptom_id: int, db: Session = Depends(get_db)):
    obj = delete_symptom(db, symptom_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Symptom not found")
    return obj
