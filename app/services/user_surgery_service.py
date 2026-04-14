from sqlalchemy.orm import Session, joinedload
from typing import Optional
from app.models.user_surgery import UserSurgery
from app.models.surgery import SurgeryCatalog


def get_or_create_surgery_catalog(db: Session, name: str, user_id: Optional[int] = None):
    catalog = db.query(SurgeryCatalog).filter(SurgeryCatalog.name == name).first()
    if catalog:
        return catalog
    catalog = SurgeryCatalog(name=name, is_custom=True, created_by_user_id=user_id)
    db.add(catalog)
    db.commit()
    db.refresh(catalog)
    return catalog


def get_user_surgeries(db: Session, user_id: int, skip: int = 0, limit: int = 100, condition_id: Optional[int] = None):
    query = db.query(UserSurgery).options(joinedload(UserSurgery.surgery)).filter(UserSurgery.user_id == user_id)
    if condition_id is not None:
        query = query.filter(UserSurgery.user_condition_id == condition_id)
    return query.offset(skip).limit(limit).all()


def get_user_surgery(db: Session, us_id: int, user_id: int):
    return db.query(UserSurgery).options(joinedload(UserSurgery.surgery)).filter(
        UserSurgery.id == us_id,
        UserSurgery.user_id == user_id
    ).first()


def create_user_surgery(
    db: Session,
    user_id: int,
    surgery_id: Optional[int] = None,
    name: Optional[str] = None,
    user_condition_id: Optional[int] = None,
    surgery_date: Optional[str] = None,
    notes: Optional[str] = None,
):
    if surgery_id is None and name is not None:
        catalog = get_or_create_surgery_catalog(db, name, user_id)
        surgery_id = catalog.id
    elif surgery_id is not None:
        catalog = db.get(SurgeryCatalog, surgery_id)
        if not catalog:
            raise ValueError("Surgery catalog entry not found")
    else:
        raise ValueError("Either surgery_id or name must be provided")

    item = UserSurgery(
        user_id=user_id,
        surgery_id=surgery_id,
        user_condition_id=user_condition_id,
        surgery_date=surgery_date,
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
    db_obj = db.query(UserSurgery).filter(
        UserSurgery.id == us_id,
        UserSurgery.user_id == user_id
    ).first()

    if not db_obj:
        return None

    for field, value in updates.items():
        setattr(db_obj, field, value)

    db.commit()
    db.refresh(db_obj)
    return db_obj
