from sqlalchemy.orm import Session
from app.models.user_profile import UserProfile
from typing import Optional
from app.models.enums import SexEnum
from datetime import date
from app.schemas.user_profile import UserProfileCreate



def get_profile(db: Session, user_id: int):
    return db.query(UserProfile).filter_by(user_id=user_id).first()


def create_profile(db: Session, user_id: int, data: UserProfileCreate):

    existing = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if existing:
        raise ValueError("Profile already exists")

    item = UserProfile(
        user_id=user_id,
        **data.model_dump()
    )

    try:
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    except:
        db.rollback()
        raise

def update_profile(db: Session, user_id: int, updates: dict):
    db_obj = get_profile(db, user_id)
    if not db_obj:
        return None

    allowed_fields = {"full_name", "birth_date", "sex", "weight", "height"}

    for field, value in updates.items():
        if field in allowed_fields:
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
