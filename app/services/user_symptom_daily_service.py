from sqlalchemy.orm import Session
from app.models.user_symptom import UserSymptom
from app.models.user_symptom_daily import UserSymptomDaily
from typing import Optional
from datetime import date


def get_user_symptom_daily_records(db: Session, user_symptom_id: int, user_id: int, skip: int = 0, limit: int = 100):
    """Obtener todos los registros diarios de un síntoma"""
    # Verificar que el síntoma pertenece al usuario
    symptom = db.query(UserSymptom).filter(
        UserSymptom.id == user_symptom_id,
        UserSymptom.user_id == user_id
    ).first()
    
    if not symptom:
        return None
    
    return db.query(UserSymptomDaily).filter(
        UserSymptomDaily.user_symptom_id == user_symptom_id
    ).offset(skip).limit(limit).all()


def get_user_symptom_daily(db: Session, daily_id: int, user_symptom_id: int, user_id: int):
    """Obtener un registro diario específico"""
    # Verificar que el síntoma pertenece al usuario
    symptom = db.query(UserSymptom).filter(
        UserSymptom.id == user_symptom_id,
        UserSymptom.user_id == user_id
    ).first()
    
    if not symptom:
        return None
    
    return db.query(UserSymptomDaily).filter(
        UserSymptomDaily.id == daily_id,
        UserSymptomDaily.user_symptom_id == user_symptom_id
    ).first()


def create_user_symptom_daily(
    db: Session,
    user_symptom_id: int,
    user_id: int,
    date_record: date,
    severity: int,
    notes: Optional[str] = None
):
    """Crear un registro diario y actualizar la severidad actual del síntoma"""
    # Verificar que el síntoma pertenece al usuario
    user_symptom = db.query(UserSymptom).filter(
        UserSymptom.id == user_symptom_id,
        UserSymptom.user_id == user_id
    ).first()
    
    if not user_symptom:
        return None
    
    # Crear el registro diario
    daily_record = UserSymptomDaily(
        user_symptom_id=user_symptom_id,
        date=date_record,
        severity=severity,
        notes=notes
    )
    
    db.add(daily_record)
    
    # Actualizar la severidad actual en UserSymptom
    user_symptom.severity = severity
    
    db.commit()
    db.refresh(daily_record)
    return daily_record


def update_user_symptom_daily(
    db: Session,
    daily_id: int,
    user_symptom_id: int,
    user_id: int,
    updates: dict
):
    """Actualizar un registro diario y sincronizar severidad si es necesario"""
    # Verificar que el síntoma pertenece al usuario
    user_symptom = db.query(UserSymptom).filter(
        UserSymptom.id == user_symptom_id,
        UserSymptom.user_id == user_id
    ).first()
    
    if not user_symptom:
        return None
    
    daily_record = db.query(UserSymptomDaily).filter(
        UserSymptomDaily.id == daily_id,
        UserSymptomDaily.user_symptom_id == user_symptom_id
    ).first()
    
    if not daily_record:
        return None
    
    for field, value in updates.items():
        setattr(daily_record, field, value)
    
    # Si se actualiza la severidad, sincronizar con UserSymptom (si es el registro más reciente)
    if "severity" in updates:
        latest_record = db.query(UserSymptomDaily).filter(
            UserSymptomDaily.user_symptom_id == user_symptom_id
        ).order_by(UserSymptomDaily.date.desc()).first()
        
        if latest_record.id == daily_record.id:
            user_symptom.severity = updates["severity"]
    
    db.commit()
    db.refresh(daily_record)
    return daily_record


def delete_user_symptom_daily(db: Session, daily_id: int, user_symptom_id: int, user_id: int):
    """Eliminar un registro diario y actualizar severity si es necesario"""
    # Verificar que el síntoma pertenece al usuario
    user_symptom = db.query(UserSymptom).filter(
        UserSymptom.id == user_symptom_id,
        UserSymptom.user_id == user_id
    ).first()
    
    if not user_symptom:
        return None
    
    daily_record = db.query(UserSymptomDaily).filter(
        UserSymptomDaily.id == daily_id,
        UserSymptomDaily.user_symptom_id == user_symptom_id
    ).first()
    
    if not daily_record:
        return None
    
    was_latest = daily_record.date == db.query(UserSymptomDaily).filter(
        UserSymptomDaily.user_symptom_id == user_symptom_id
    ).order_by(UserSymptomDaily.date.desc()).first().date
    
    db.delete(daily_record)
    
    # Si era el más reciente, actualizar severity al anterior más reciente (si existe)
    if was_latest:
        previous_record = db.query(UserSymptomDaily).filter(
            UserSymptomDaily.user_symptom_id == user_symptom_id
        ).order_by(UserSymptomDaily.date.desc()).first()
        
        if previous_record:
            user_symptom.severity = previous_record.severity
        else:
            user_symptom.severity = None
    
    db.commit()
    return daily_record
