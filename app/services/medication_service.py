from sqlalchemy.orm import Session
from app.models.medication import MedicationCatalog


def get_medications(db: Session, skip: int = 0, limit: int = 100):
    return db.query(MedicationCatalog).offset(skip).limit(limit).all()


def get_medication(db: Session, medication_id: int):
    return db.query(MedicationCatalog).filter(MedicationCatalog.id == medication_id).first()


def create_medication(db: Session, name: str, is_custom: bool = False, created_by_user_id: int | None = None):
    item = MedicationCatalog(name=name, is_custom=is_custom, created_by_user_id=created_by_user_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def delete_medication(db: Session, medication_id: int):
    obj = get_medication(db, medication_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
