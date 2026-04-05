from sqlalchemy.orm import Session
from app.models.symptom import SymptomCatalog
from sqlalchemy import or_, false


def get_symptoms(db: Session, user_id: int | None = None, skip: int = 0, limit: int = 100):
    # list global symptoms and, if user_id provided, include that user's custom entries
    query = db.query(SymptomCatalog)
    if user_id is not None:
        from sqlalchemy import or_, false
        query = query.filter(
            or_(
                SymptomCatalog.is_custom == false(),
                SymptomCatalog.is_custom.is_(None),
                SymptomCatalog.created_by_user_id == user_id,
            )
        )
    return query.offset(skip).limit(limit).all()


def get_symptom(db: Session, symptom_id: int, user_id: int | None = None):
    query = db.query(SymptomCatalog).filter(SymptomCatalog.id == symptom_id)
    if user_id is not None:
        
        query = query.filter(
            or_(
                SymptomCatalog.is_custom == false(),
                SymptomCatalog.created_by_user_id == user_id,
            )
        )
    return query.first()


def create_symptom(db: Session, name: str, user_id: int, is_custom: bool = False):
    # only authenticated user can create; created_by_user_id set to caller
    item = SymptomCatalog(name=name, is_custom=is_custom, created_by_user_id=user_id if is_custom else None)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def delete_symptom(db: Session, symptom_id: int, user_id: int):
    obj = get_symptom(db, symptom_id, user_id)
    if not obj:
        return None
    # only allow deletion of custom symptoms by creator
    if obj.is_custom and obj.created_by_user_id == user_id:
        db.delete(obj)
        db.commit()
        return obj
    # if not custom or not owner, refuse
    return None
