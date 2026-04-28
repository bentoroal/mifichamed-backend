from fastapi import APIRouter, Depends, HTTPException, Response
from typing import List
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.condition_treatment import (
    ConditionTreatmentCreate,
    ConditionTreatmentResponse,
    ConditionTreatmentUpdate,
)
from app.services.condition_treatment_service import (
    get_treatments,
    get_treatment,
    create_treatment,
    delete_treatment,
    update_treatment,
)
from app.db.session import get_db

router = APIRouter(prefix="/condition-treatments", tags=["ConditionTreatments"])

#Ruta para obtener la lista de tratamientos de una condición médica, con paginación
@router.get("/", response_model=List[ConditionTreatmentResponse])
def list_treatments(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_treatments(db, current_user.id, skip, limit)

#Ruta para crear un nuevo tratamiento para una condición médica
@router.post("/", response_model=ConditionTreatmentResponse)
def create(
    item: ConditionTreatmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    res = create_treatment(
        db,
        current_user.id,
        item.user_condition_id,
        item.medication_id,
        item.dosage,
        item.frequency,
        item.start_date,
        item.end_date,
        item.notes,
    )
    if res is None:
        raise HTTPException(status_code=403, detail="UserCondition does not belong to current user")
    return res

#Ruta para obtener un tratamiento específico por su ID
@router.get("/{t_id}", response_model=ConditionTreatmentResponse)
def read(
    t_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_obj = get_treatment(db, t_id, current_user.id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Treatment not found")
    return db_obj

#Ruta para eliminar un tratamiento específico por su ID
@router.delete("/{t_id}", response_model=ConditionTreatmentResponse)
def remove(
    t_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    obj = delete_treatment(db, t_id, current_user.id)
    if not obj:
        raise HTTPException(status_code=404, detail="ConditionTreatment not found or not owned")
    return Response(status_code=204)


@router.patch("/{t_id}", response_model=ConditionTreatmentResponse)
def update(
    t_id: int,
    item: ConditionTreatmentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        db_obj = update_treatment(
            db,
            t_id,
            current_user.id,
            item.model_dump(exclude_unset=True),
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if not db_obj:
        raise HTTPException(status_code=404, detail="ConditionTreatment not found or not owned")
    return db_obj
