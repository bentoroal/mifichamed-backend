from sqlalchemy import Session
from app.models.allergy import AllergyCatalog

def get_allergies(db: Session, user_id: int | None = None, skip: int = 0, limit: int = 100):
    # list global allergies and, if user_id provided, include that user's custom entries
    query = db.query(AllergyCatalog)
    if user_id is not None:
        from sqlalchemy import or_, false
        query = query.filter(
            or_(
                AllergyCatalog.is_custom == false(),
                AllergyCatalog.created_by_user_id == user_id,
            )
        )
    return query.offset(skip).limit(limit).all()

def get_allergy(db: Session, allergy_id: int, user_id: int | None = None):
    query = db.query(AllergyCatalog).filter(AllergyCatalog.id == allergy_id)
    if user_id is not None:
        from sqlalchemy import or_, false
        query = query.filter(
            or_(
                AllergyCatalog.is_custom == false(),
                AllergyCatalog.created_by_user_id == user_id,
            )
        )
    return query.first()

def create_allergy(db: Session, name: str, user_id: int, is_custom: bool = False):
    # only authenticated user can create; created_by_user_id set to caller
    item = AllergyCatalog(name=name, is_custom=is_custom, created_by_user_id=user_id if is_custom else None)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def delete_allergy(db: Session, allergy_id: int, user_id: int):
    obj = get_allergy(db, allergy_id, user_id)
    if not obj:
        return None
    # only allow deletion of custom allergies by creator
    if obj.is_custom and obj.created_by_user_id == user_id:
        db.delete(obj)
        db.commit()
        return obj
    # if not custom or not owner, refuse
    return None