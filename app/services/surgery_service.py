from sqlalchemy.orm import Session
from typing import Optional
from app.models.user_surgery import UserSurgery
from app.models.surgery import SurgeryCatalog

def get_user_surgeries(db: Session, user_id: int, skip: int = 0, limit: int = 100, condition_id: Optional[int] = None):
    query = db.query(UserSurgery).filter(UserSurgery.user_id == user_id)
    if condition_id is not None:
        query = query.filter(UserSurgery.user_condition_id == condition_id)
    return query.offset(skip).limit(limit).all()

def get_user_surgery(db: Session, us_id: int, user_id: int):
    return db.query(UserSurgery).filter(UserSurgery.id == us_id, UserSurgery.user_id == user_id).first()

def create_user_surgery(
    db: Session,
    user_id: int,
    surgery_id: Optional[int] = None,
    name: Optional[str] = None,
    user_condition_id: Optional[int] = None,
    surgery_date: Optional[str] = None,
    status: Optional[str] = None,
    notes: Optional[str] = None,
):
    # Si no se pasa surgery_id, crear en catálogo
    if surgery_id is None:
        if not name:
            return None
        new_surg = SurgeryCatalog(name=name, is_custom=True, created_by_user_id=user_id)
        db.add(new_surg)
        db.commit()
        db.refresh(new_surg)
        surgery_id = new_surg.id

    item = UserSurgery(
        user_id=user_id,
        surgery_id=surgery_id,
        user_condition_id=user_condition_id,
        surgery_date=surgery_date,
        status=status,
        notes=notes,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def delete_user_surgery(db: Session, us_id: int, user_id: int):
    obj = get_user_surgery(db, us_id, user_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj

def update_user_surgery(db: Session, us_id: int, user_id: int, updates: dict):
    db_obj = db.query(UserSurgery).filter(UserSurgery.id == us_id, UserSurgery.user_id == user_id).first()
    if not db_obj:
        return None

    # soporte para crear un catálogo si envían "name"
    if "name" in updates and updates.get("name"):
        new_surg = SurgeryCatalog(name=updates["name"], is_custom=True, created_by_user_id=user_id)
        db.add(new_surg)
        db.commit()
        db.refresh(new_surg)
        updates["surgery_id"] = new_surg.id
        updates.pop("name", None)

    for field, value in updates.items():
        setattr(db_obj, field, value)

    db.commit()
    db.refresh(db_obj)
    return db_obj