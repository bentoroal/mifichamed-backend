from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.schemas.medication import MedicationCatalogCreate, MedicationCatalogResponse
from app.services.medication_service import get_medications, get_medication, create_medication, delete_medication
from app.db.session import get_db

router = APIRouter(prefix="/medications", tags=["Medications"])


@router.get("/", response_model=List[MedicationCatalogResponse])
def list_medications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_medications(db, skip, limit)


@router.post("/", response_model=MedicationCatalogResponse)
def create(item: MedicationCatalogCreate, db: Session = Depends(get_db)):
    return create_medication(db, item.name, item.is_custom, item.created_by_user_id)


@router.get("/{medication_id}", response_model=MedicationCatalogResponse)
def read(medication_id: int, db: Session = Depends(get_db)):
    db_obj = get_medication(db, medication_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Medication not found")
    return db_obj


@router.delete("/{medication_id}", response_model=MedicationCatalogResponse)
def remove(medication_id: int, db: Session = Depends(get_db)):
    obj = delete_medication(db, medication_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Medication not found")
    return obj
