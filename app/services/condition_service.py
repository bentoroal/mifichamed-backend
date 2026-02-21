from sqlalchemy.orm import Session
from app.models.condition import ConditionCatalog


def get_conditions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ConditionCatalog).offset(skip).limit(limit).all()


def get_condition(db: Session, condition_id: int):
    return db.query(ConditionCatalog).filter(ConditionCatalog.id == condition_id).first()


def create_condition(db: Session, name: str, is_custom: bool = False, created_by_user_id: int | None = None):
    cond = ConditionCatalog(name=name, is_custom=is_custom, created_by_user_id=created_by_user_id)
    db.add(cond)
    db.commit()
    db.refresh(cond)
    return cond


def delete_condition(db: Session, condition_id: int):
    obj = get_condition(db, condition_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
