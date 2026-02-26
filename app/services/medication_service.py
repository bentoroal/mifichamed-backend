from sqlalchemy.orm import Session
from app.models.medication import MedicationCatalog


def get_medications(db: Session, user_id: int | None = None, skip: int = 0, limit: int = 100):
    # return global medications plus any custom ones owned by user
    query = db.query(MedicationCatalog)
    if user_id is not None:
        from sqlalchemy import or_, false
        query = query.filter(
            or_(
                MedicationCatalog.is_custom == false(),
                MedicationCatalog.created_by_user_id == user_id,
            )
        )
    return query.offset(skip).limit(limit).all()


def get_medication(db: Session, medication_id: int, user_id: int | None = None):
    query = db.query(MedicationCatalog).filter(MedicationCatalog.id == medication_id)
    if user_id is not None:
        from sqlalchemy import or_, false
        query = query.filter(
            or_(
                MedicationCatalog.is_custom == false(),
                MedicationCatalog.created_by_user_id == user_id,
            )
        )
    return query.first()


def create_medication(db: Session, name: str, user_id: int, is_custom: bool = False):
    # created_by_user_id only set when custom flag true
    item = MedicationCatalog(name=name, is_custom=is_custom, created_by_user_id=user_id if is_custom else None)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def delete_medication(db: Session, medication_id: int, user_id: int):
    obj = get_medication(db, medication_id, user_id)
    if not obj:
        return None
    # only custom medications can be deleted and only by creator
    if obj.is_custom and obj.created_by_user_id == user_id:
        db.delete(obj)
        db.commit()
        return obj
    return None
