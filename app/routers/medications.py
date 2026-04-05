from fastapi import APIRouter, Depends, HTTPException, Response
from typing import List
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.medication import MedicationCatalogCreate, MedicationCatalogResponse
from app.services.medication_service import get_medications, get_medication, create_medication, delete_medication
from app.db.session import get_db

router = APIRouter(prefix="/medications", tags=["Medications"])


@router.get("/", response_model=List[MedicationCatalogResponse])
def list_medications(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_medications(db, current_user.id, skip, limit)


@router.post("/", response_model=MedicationCatalogResponse)
def create(
    item: MedicationCatalogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # ignore any user id from request body
    return create_medication(db, item.name, current_user.id, item.is_custom)


@router.get("/{medication_id}", response_model=MedicationCatalogResponse)
def read(
    medication_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_obj = get_medication(db, medication_id, current_user.id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Medication not found")
    return db_obj


@router.delete("/{medication_id}", response_model=MedicationCatalogResponse)
def remove(
    medication_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    obj = delete_medication(db, medication_id, current_user.id)
    if not obj:
        raise HTTPException(status_code=404, detail="Medication not found or not owned")
    return Response(status_code=204)
