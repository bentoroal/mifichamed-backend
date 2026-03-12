from sqlalchemy.orm import Session
from typing import Optional
from app.models.user_allergy import UserAllergy
from app.models.allergy import AllergyCatalog

def get_user_allergies(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(UserAllergy).filter(UserAllergy.user_id == user_id).offset(skip).limit(limit).all()

def get_user_allergy(db: Session, ua_id: int, user_id: int):
    return db.query(UserAllergy).filter(
        UserAllergy.id == ua_id,
        UserAllergy.user_id == user_id
    ).first()

def create_user_allergy(
    db: Session,
    user_id: int,
    allergy_id: Optional[int] = None,
    name: Optional[str] = None,
    status: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    notes: Optional[str] = None,
):
    if allergy_id is None:
        if not name:
            return None
        new_allergy = AllergyCatalog(name=name, is_custom=True, created_by_user_id=user_id)
        db.add(new_allergy)
        db.commit()
        db.refresh(new_allergy)
        allergy_id = new_allergy.id

    item = UserAllergy(
        user_id=user_id,
        allergy_id=allergy_id,
        status=status,
        start_date=start_date,
        end_date=end_date,
        notes=notes,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def delete_user_allergy(db: Session, ua_id: int, user_id: int):
    obj = get_user_allergy(db, ua_id, user_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj

def update_user_allergy(db: Session, ua_id: int, user_id: int, updates: dict):
    db_obj = db.query(UserAllergy).filter(
        UserAllergy.id == ua_id,
        UserAllergy.user_id == user_id
    ).first()

    if not db_obj:
        return None

    # Si actualizan por name -> crear entrada en catálogo y actualizar allergy_id
    if "name" in updates and updates.get("name"):
        new_allergy = AllergyCatalog(name=updates["name"], is_custom=True, created_by_user_id=user_id)
        db.add(new_allergy)
        db.commit()
        db.refresh(new_allergy)
        updates["allergy_id"] = new_allergy.id
        updates.pop("name", None)

    for field, value in updates.items():
        setattr(db_obj, field, value)

    db.commit()
    db.refresh(db_obj)
    return db_obj