from sqlalchemy.orm import Session
from app.models.user_profile import UserProfile
from typing import Optional


def get_profile(db: Session, user_id: int):
    return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()


def create_profile(
        db: Session,
        user_id: int, 
        full_name: str, 
        birth_date: Optional[str] = None, 
        sex: Optional[str] = None,
        weight: Optional[int] = None,
        height: Optional[int] = None):
    
    item = UserProfile(
        user_id=user_id,
        full_name=full_name,
        birth_date=birth_date,
        sex=sex,
        weight=weight,
        height=height
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_profile(db: Session, user_id: int, updates: dict):
    db_obj = get_profile(db, user_id)
    if not db_obj:
        return None

    for field, value in updates.items():
        setattr(db_obj, field, value)

    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_profile(db: Session, user_id: int):
    obj = get_profile(db, user_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
