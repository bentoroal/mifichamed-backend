from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.enums import ExamType
from app.models.user import User
from app.schemas.exam_result import (
    ExamResultBulkCreate,
    ExamResultCreate,
    ExamResultResponse,
    ExamResultUpdate,
)
from app.services.exam_result_service import (
    create_exam_result,
    create_exam_results,
    delete_exam_result,
    get_exam_result,
    get_exam_results,
    update_exam_result,
)

router = APIRouter(prefix="/exam-results", tags=["ExamResults"])


@router.get("/types")
def list_exam_types():
    return [exam_type.value for exam_type in ExamType]


@router.get("/", response_model=List[ExamResultResponse])
def list_results(
    skip: int = 0,
    limit: int = 100,
    exam_type: Optional[ExamType] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_exam_results(db, current_user.id, skip, limit, exam_type, search)


@router.post("/", response_model=ExamResultResponse)
def create(
    item: ExamResultCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_exam_result(
        db,
        current_user.id,
        item.name,
        item.exam_type,
        item.result,
        item.exam_date,
        item.notes,
    )


@router.post("/bulk", response_model=List[ExamResultResponse])
def create_bulk(
    payload: ExamResultBulkCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    items = [item.model_dump() for item in payload.items]
    return create_exam_results(db, current_user.id, items)


@router.get("/{exam_result_id}", response_model=ExamResultResponse)
def read(
    exam_result_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    item = get_exam_result(db, exam_result_id, current_user.id)
    if not item:
        raise HTTPException(status_code=404, detail="Exam result not found")
    return item


@router.patch("/{exam_result_id}", response_model=ExamResultResponse)
def update(
    exam_result_id: int,
    item: ExamResultUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    updated = update_exam_result(
        db,
        exam_result_id,
        current_user.id,
        item.model_dump(exclude_unset=True),
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Exam result not found")
    return updated


@router.delete("/{exam_result_id}", status_code=204)
def remove(
    exam_result_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    deleted = delete_exam_result(db, exam_result_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Exam result not found")
    return Response(status_code=204)