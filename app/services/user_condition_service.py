from sqlalchemy.orm import Session
from app.models.user_condition import UserCondition
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


def create_user_condition(db: Session, user_id: int, condition_id: int, diagnosis_date: Optional[str] = None, status: Optional[ConditionStatus] = ConditionStatus.ACTIVE, notes: Optional[str] = None):
    item = UserCondition(user_id=user_id, condition_id=condition_id, diagnosis_date=diagnosis_date, status=status, notes=notes)
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
