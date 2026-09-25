from typing import Optional

from sqlalchemy.orm import Session

from app.models.enums import ExamType
from app.models.exam_result import ExamResult


def get_exam_results(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    exam_type: Optional[ExamType] = None,
    search: Optional[str] = None,
):
    query = db.query(ExamResult).filter(ExamResult.user_id == user_id)
    if exam_type is not None:
        query = query.filter(ExamResult.exam_type == exam_type)
    if search:
        query = query.filter(ExamResult.name.ilike(f"%{search}%"))
    return query.order_by(ExamResult.exam_date.desc(), ExamResult.id.desc()).offset(skip).limit(limit).all()


def get_exam_result(db: Session, exam_result_id: int, user_id: int):
    return db.query(ExamResult).filter(
        ExamResult.id == exam_result_id,
        ExamResult.user_id == user_id,
    ).first()


def create_exam_result(
    db: Session,
    user_id: int,
    name: str,
    exam_type: ExamType,
    result: str,
    exam_date=None,
    notes: Optional[str] = None,
):
    item = ExamResult(
        user_id=user_id,
        name=name.strip(),
        exam_type=exam_type,
        result=result.strip(),
        exam_date=exam_date,
        notes=notes,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def create_exam_results(
    db: Session,
    user_id: int,
    items: list[dict],
):
    exam_results = [
        ExamResult(
            user_id=user_id,
            name=item["name"].strip(),
            exam_type=item["exam_type"],
            result=item["result"].strip(),
            exam_date=item.get("exam_date"),
            notes=item.get("notes"),
        )
        for item in items
    ]
    db.add_all(exam_results)
    db.commit()
    for exam_result in exam_results:
        db.refresh(exam_result)
    return exam_results


def update_exam_result(db: Session, exam_result_id: int, user_id: int, updates: dict):
    item = get_exam_result(db, exam_result_id, user_id)
    if not item:
        return None

    if "name" in updates and updates["name"] is not None:
        updates["name"] = updates["name"].strip()
    if "result" in updates and updates["result"] is not None:
        updates["result"] = updates["result"].strip()

    for field, value in updates.items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


def delete_exam_result(db: Session, exam_result_id: int, user_id: int):
    item = get_exam_result(db, exam_result_id, user_id)
    if not item:
        return None
    db.delete(item)
    db.commit()
    return item