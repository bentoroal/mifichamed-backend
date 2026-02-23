from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.schemas.condition_treatment import ConditionTreatmentCreate, ConditionTreatmentResponse
from app.services.condition_treatment_service import get_treatments, get_treatment, create_treatment, delete_treatment
from app.db.session import get_db

router = APIRouter(prefix="/condition-treatments", tags=["ConditionTreatments"])

#Ruta para obtener la lista de tratamientos de una condición médica, con paginación
@router.get("/", response_model=List[ConditionTreatmentResponse])
def list_treatments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_treatments(db, skip, limit)

#Ruta para crear un nuevo tratamiento para una condición médica
@router.post("/", response_model=ConditionTreatmentResponse)
def create(item: ConditionTreatmentCreate, db: Session = Depends(get_db)):
    return create_treatment(db, item.user_condition_id, item.medication_id, item.dosage, item.frequency, item.start_date, item.end_date, item.notes)

#Ruta para obtener un tratamiento específico por su ID
@router.get("/{t_id}", response_model=ConditionTreatmentResponse)
def read(t_id: int, db: Session = Depends(get_db)):
    db_obj = get_treatment(db, t_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Treatment not found")
    return db_obj

#Ruta para eliminar un tratamiento específico por su ID
@router.delete("/{t_id}", response_model=ConditionTreatmentResponse)
def remove(t_id: int, db: Session = Depends(get_db)):
    obj = delete_treatment(db, t_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Treatment not found")
    return obj
