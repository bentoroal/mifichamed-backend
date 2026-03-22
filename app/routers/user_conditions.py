from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user_condition import UserConditionCreate, UserConditionResponse
from app.schemas.user_symptom import UserSymptomResponse
from app.services.user_condition_service import (
    get_user_conditions,
    get_user_condition,
    create_user_condition,
    delete_user_condition,
    get_active_symptoms_for_condition,
)
from app.db.session import get_db

router = APIRouter(prefix="/user-conditions", tags=["UserConditions"])


@router.get("/", response_model=List[UserConditionResponse])
def list_user_conditions(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_user_conditions(db, current_user.id, skip, limit)


@router.post("/", response_model=UserConditionResponse)
def create(
    item: UserConditionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # ignore user_id from request, always use authenticated user
    return create_user_condition(
        db,
        current_user.id,
        item.condition_id,
        item.start_date,
        item.end_date,
        item.status,
        item.notes,
    )


@router.get("/{uc_id}", response_model=UserConditionResponse)
def read(
    uc_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_obj = get_user_condition(db, uc_id, current_user.id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="UserCondition not found")
    return db_obj


@router.delete("/{uc_id}", response_model=UserConditionResponse)
def remove(
    uc_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    obj = delete_user_condition(db, uc_id, current_user.id)
    if not obj:
        raise HTTPException(status_code=404, detail="UserCondition not found")
    return obj


# ENDPOINT PARA OBTENER SÍNTOMAS ACTIVOS DURANTE UNA CONDICIÓN
# Este endpoint devuelve todos los síntomas del usuario que estuvieron activos durante 
# el período de una condición específica, basándose en el solapamiento de fechas.
@router.get("/{uc_id}/symptoms", response_model=List[UserSymptomResponse])
def get_condition_symptoms(
    uc_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Obtiene los síntomas que estuvieron activos durante la vigencia de una condición.
    
    Busca todos los síntomas del usuario cuyo rango de fechas (start_date - end_date)
    se superpone con el rango de la condición (start_date - end_date).
    
    Esto permite visualizar en el frontend qué síntomas estuvo experimentando el usuario
    mientras tenía una condición específica.
    """
    # Buscar síntomas activos durante la vigencia de la condición
    symptoms = get_active_symptoms_for_condition(db, uc_id, current_user.id, skip, limit)
    
    # Retornar 404 si la condición no existe o no pertenece al usuario
    if symptoms is None:
        raise HTTPException(status_code=404, detail="UserCondition not found")
    
    return symptoms
