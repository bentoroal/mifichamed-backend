from sqlalchemy.orm import Session
from app.models.condition_treatment import ConditionTreatment
from typing import Optional


def get_treatments(db: Session, user_id: int | None = None, skip: int = 0, limit: int = 100):
    # if user_id provided, only return treatments belonging to that user's conditions
    query = db.query(ConditionTreatment)
    if user_id is not None:
        from sqlalchemy.orm import joinedload
        from app.models.user_condition import UserCondition
        query = query.join(UserCondition).filter(UserCondition.user_id == user_id)
    return query.offset(skip).limit(limit).all()


def get_treatment(db: Session, t_id: int, user_id: int | None = None):
    query = db.query(ConditionTreatment).filter(ConditionTreatment.id == t_id)
    if user_id is not None:
        from app.models.user_condition import UserCondition
        query = query.join(UserCondition).filter(UserCondition.user_id == user_id)
    return query.first()


def create_treatment(db: Session, user_id: int, user_condition_id: int, medication_id: Optional[int] = None, dosage: Optional[str] = None, frequency: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, notes: Optional[str] = None):
    # verify that the given condition belongs to the user
    from app.models.user_condition import UserCondition
    cond = db.query(UserCondition).filter(
        UserCondition.id == user_condition_id,
        UserCondition.user_id == user_id
    ).first()
    if not cond:
        return None
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


def delete_treatment(db: Session, t_id: int, user_id: int):
    obj = get_treatment(db, t_id, user_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
