from sqlalchemy.orm import Session
from app.models.user_symptom import UserSymptom
from app.models.user_symptom_daily import UserSymptomDaily
from typing import Optional
from datetime import date


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def _get_user_symptom(db: Session, user_symptom_id: int, user_id: int):
    return db.query(UserSymptom).filter(
        UserSymptom.id == user_symptom_id,
        UserSymptom.user_id == user_id
    ).first()


def _sync_latest_severity(db: Session, user_symptom_id: int):
    latest = db.query(UserSymptomDaily).filter(
        UserSymptomDaily.user_symptom_id == user_symptom_id
    ).order_by(UserSymptomDaily.date.desc()).first()

    symptom = db.query(UserSymptom).filter(
        UserSymptom.id == user_symptom_id
    ).first()

    if symptom:
        symptom.severity = latest.severity if latest else None


# --------------------------------------------------
# GET
# --------------------------------------------------

def get_user_symptom_daily_records(
    db: Session,
    user_symptom_id: int,
    user_id: int,
    skip: int = 0,
    limit: int = 100
):
    symptom = _get_user_symptom(db, user_symptom_id, user_id)
    if not symptom:
        return None

    return db.query(UserSymptomDaily).filter(
        UserSymptomDaily.user_symptom_id == user_symptom_id
    ).order_by(UserSymptomDaily.date.desc()).offset(skip).limit(limit).all()


def get_user_symptom_daily(
    db: Session,
    daily_id: int,
    user_symptom_id: int,
    user_id: int
):
    symptom = _get_user_symptom(db, user_symptom_id, user_id)
    if not symptom:
        return None

    return db.query(UserSymptomDaily).filter(
        UserSymptomDaily.id == daily_id,
        UserSymptomDaily.user_symptom_id == user_symptom_id
    ).first()


def get_user_symptom_daily_by_date(
    db: Session,
    user_symptom_id: int,
    user_id: int,
    date_record: date
):
    symptom = _get_user_symptom(db, user_symptom_id, user_id)
    if not symptom:
        return None

    return db.query(UserSymptomDaily).filter(
        UserSymptomDaily.user_symptom_id == user_symptom_id,
        UserSymptomDaily.date == date_record
    ).first()


# --------------------------------------------------
# UPSERT 
# --------------------------------------------------

def create_user_symptom_daily(
    db: Session,
    user_symptom_id: int,
    user_id: int,
    date_record: date,
    severity: int,
    notes: Optional[str] = None
):
    symptom = _get_user_symptom(db, user_symptom_id, user_id)
    if not symptom:
        return None

    # 🔥 BUSCAR SI YA EXISTE
    existing = db.query(UserSymptomDaily).filter(
        UserSymptomDaily.user_symptom_id == user_symptom_id,
        UserSymptomDaily.date == date_record
    ).first()

    if existing:
        # UPDATE
        existing.severity = severity
        if notes is not None:
            existing.notes = notes
        record = existing

    else:
        # CREATE
        record = UserSymptomDaily(
            user_symptom_id=user_symptom_id,
            date=date_record,
            severity=severity,
            notes=notes
        )
        db.add(record)

    # 🔄 sync severity global
    _sync_latest_severity(db, user_symptom_id)

    db.commit()
    db.refresh(record)
    return record


# --------------------------------------------------
# UPDATE
# --------------------------------------------------

def update_user_symptom_daily(
    db: Session,
    daily_id: int,
    user_symptom_id: int,
    user_id: int,
    updates: dict
):
    symptom = _get_user_symptom(db, user_symptom_id, user_id)
    if not symptom:
        return None

    record = db.query(UserSymptomDaily).filter(
        UserSymptomDaily.id == daily_id,
        UserSymptomDaily.user_symptom_id == user_symptom_id
    ).first()

    if not record:
        return None

    for field, value in updates.items():
        setattr(record, field, value)

    _sync_latest_severity(db, user_symptom_id)

    db.commit()
    db.refresh(record)
    return record


# --------------------------------------------------
# DELETE
# --------------------------------------------------

def delete_user_symptom_daily(
    db: Session,
    daily_id: int,
    user_symptom_id: int,
    user_id: int
):
    symptom = _get_user_symptom(db, user_symptom_id, user_id)
    if not symptom:
        return None

    record = db.query(UserSymptomDaily).filter(
        UserSymptomDaily.id == daily_id,
        UserSymptomDaily.user_symptom_id == user_symptom_id
    ).first()

    if not record:
        return None

    db.delete(record)

    _sync_latest_severity(db, user_symptom_id)

    db.commit()
    return record