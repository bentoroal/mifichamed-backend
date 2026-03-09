from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.user_condition import UserCondition
from app.models.user_symptom import UserSymptom
from app.models.enums import ConditionStatus
from typing import Optional


def get_user_conditions(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    # return paginated list of conditions for a specific user
    return db.query(UserCondition).filter(
        UserCondition.user_id == user_id
    ).offset(skip).limit(limit).all()


def get_user_condition(db: Session, uc_id: int, user_id: int):
    return db.query(UserCondition).filter(
        UserCondition.id == uc_id,
        UserCondition.user_id == user_id
    ).first()


def create_user_condition(db: Session, user_id: int, condition_id: int, diagnosis_date: Optional[str] = None, end_date: Optional[str] = None, status: Optional[ConditionStatus] = ConditionStatus.ACTIVE, notes: Optional[str] = None):
    item = UserCondition(user_id=user_id, condition_id=condition_id, diagnosis_date=diagnosis_date, end_date=end_date, status=status, notes=notes)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def delete_user_condition(db: Session, uc_id: int, user_id: int):
    obj = get_user_condition(db, uc_id, user_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj


def get_active_symptoms_for_condition(db: Session, uc_id: int, user_id: int, skip: int = 0, limit: int = 100):
    """
    Obtiene los síntomas que estuvieron activos durante la vigencia de una condición específica.
    
    La lógica busca síntomas del usuario cuyo rango de fechas (start_date - end_date) se superpone
    con el rango de fechas de la condición (diagnosis_date - end_date).
    
    Solapamiento de fechas:
    - (síntoma.start_date <= condición.end_date OR condición.end_date es NULL)
    - AND (síntoma.end_date >= condición.diagnosis_date OR síntoma.end_date es NULL)
    """
    # Primero obtener la condición para validar que existe y pertenece al usuario
    user_condition = get_user_condition(db, uc_id, user_id)
    if not user_condition:
        return None
    
    # Query para obtener síntomas que se solapan con el rango de la condición
    # Se considera que un síntoma está activo durante la condición si sus períodos se intersectan
    symptoms = db.query(UserSymptom).filter(
        UserSymptom.user_id == user_id,
        # El síntoma comienza antes de que termine la condición (o la condición no ha terminado)
        or_(
            UserSymptom.start_date <= user_condition.end_date,
            user_condition.end_date == None
        ),
        # El síntoma termina después de que comienza la condición (o el síntoma sigue activo)
        or_(
            UserSymptom.end_date >= user_condition.diagnosis_date,
            UserSymptom.end_date == None
        )
    ).offset(skip).limit(limit).all()
    
    return symptoms
