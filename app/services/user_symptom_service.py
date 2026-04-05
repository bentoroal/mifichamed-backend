from sqlalchemy.orm import Session
from app.models.user_symptom import UserSymptom
from typing import Optional
from sqlalchemy.orm import joinedload

def get_user_symptoms(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(UserSymptom).options(
        joinedload(UserSymptom.symptom)  # 🔥 esto faltaba
    ).filter(
        UserSymptom.user_id == user_id
    ).offset(skip).limit(limit).all()


def get_user_symptom(db: Session, us_id: int, user_id: int):
    return db.query(UserSymptom).filter(
        UserSymptom.id == us_id,
        UserSymptom.user_id == user_id
    ).first()


def create_user_symptom(db: Session, user_id: int, symptom_id: int, start_date: Optional[str] = None, end_date: Optional[str] = None, severity: Optional[int] = None, is_current: bool = True, notes: Optional[str] = None):
    item = UserSymptom(
        user_id=user_id,
        symptom_id=symptom_id,
        start_date=start_date,
        end_date=end_date,
        severity=severity,
        is_current=is_current,
        notes=notes,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def delete_user_symptom(db: Session, us_id: int, user_id: int):
    # ensure the symptom belongs to the requesting user
    obj = get_user_symptom(db, us_id, user_id)
    if not obj:
        return None

    db.delete(obj)
    db.commit()
    return obj

def update_user_symptom(db: Session, us_id: int, user_id: int, updates: dict):
    db_obj = db.query(UserSymptom).filter(
        UserSymptom.id == us_id,
        UserSymptom.user_id == user_id
    ).first()

    if not db_obj:
        return None

    for field, value in updates.items():
        setattr(db_obj, field, value)

    db.commit()
    db.refresh(db_obj)

    return db_obj
