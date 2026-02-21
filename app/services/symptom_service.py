from sqlalchemy.orm import Session
from app.models.symptom import SymptomCatalog


def get_symptoms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SymptomCatalog).offset(skip).limit(limit).all()


def get_symptom(db: Session, symptom_id: int):
    return db.query(SymptomCatalog).filter(SymptomCatalog.id == symptom_id).first()


def create_symptom(db: Session, name: str, is_custom: bool = False, created_by_user_id: int | None = None):
    item = SymptomCatalog(name=name, is_custom=is_custom, created_by_user_id=created_by_user_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def delete_symptom(db: Session, symptom_id: int):
    obj = get_symptom(db, symptom_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
