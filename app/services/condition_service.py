from sqlalchemy.orm import Session
from app.models.condition import ConditionCatalog
from app.models.enums import ConditionCategory
from typing import Optional
from sqlalchemy import or_, false

def get_conditions(
    db: Session,
    user_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    category: Optional[ConditionCategory] = None,
    search: Optional[str] = None,
):
    query = db.query(ConditionCatalog)

    if user_id is not None:
        query = query.filter(
            or_(
                ConditionCatalog.is_custom == false(),
                ConditionCatalog.created_by_user_id == user_id,
            )
        )

    # filtro por categoría
    if category:
        query = query.filter(ConditionCatalog.category == category)

    # búsqueda
    if search:
        query = query.filter(ConditionCatalog.name.ilike(f"%{search}%"))

    return query.offset(skip).limit(limit).all()


def get_condition(db: Session, condition_id: int, user_id: int | None = None):
    query = db.query(ConditionCatalog).filter(ConditionCatalog.id == condition_id)
    if user_id is not None:
        from sqlalchemy import or_, false
        query = query.filter(
            or_(
                ConditionCatalog.is_custom == false(),
                ConditionCatalog.created_by_user_id == user_id,
            )
        )
    return query.first()


def create_condition(
    db: Session,
    name: str,
    category: ConditionCategory,
    user_id: int,
    is_custom: bool = True
):
    # normalizar nombre
    normalized_name = name.strip().lower()

    existing = db.query(ConditionCatalog).filter(
        ConditionCatalog.category == category,
        ConditionCatalog.name.ilike(normalized_name),
    ).filter(
        # SOLO globales o del mismo usuario
        or_(
            ConditionCatalog.is_custom == false(),
            ConditionCatalog.created_by_user_id == user_id
        )
    ).first()

    if existing:
        return existing

    cond = ConditionCatalog(
        name=name.strip(),  # limpio
        category=category,
        is_custom=True,  # 
        created_by_user_id=user_id,
    )

    db.add(cond)
    db.commit()
    db.refresh(cond)
    return cond


def delete_condition(db: Session, condition_id: int, user_id: int):
    obj = get_condition(db, condition_id, user_id)
    if not obj:
        return None
    # only custom conditions may be deleted by their creator
    if obj.is_custom and obj.created_by_user_id == user_id:
        db.delete(obj)
        db.commit()
        return obj
    return None
