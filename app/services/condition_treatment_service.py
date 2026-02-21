from sqlalchemy.orm import Session
from app.models.condition_treatment import ConditionTreatment
from typing import Optional


def get_treatments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ConditionTreatment).offset(skip).limit(limit).all()


def get_treatment(db: Session, t_id: int):
    return db.query(ConditionTreatment).filter(ConditionTreatment.id == t_id).first()


def create_treatment(db: Session, user_condition_id: int, medication_id: Optional[int] = None, dosage: Optional[str] = None, frequency: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, notes: Optional[str] = None):
    item = ConditionTreatment(
        user_condition_id=user_condition_id,
        medication_id=medication_id,
        dosage=dosage,
        frequency=frequency,
        start_date=start_date,
        end_date=end_date,
        notes=notes,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def delete_treatment(db: Session, t_id: int):
    obj = get_treatment(db, t_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
