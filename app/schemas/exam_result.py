from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.enums import ExamType


class ExamResultBase(BaseModel):
    name: str
    exam_type: ExamType
    result: str
    exam_date: Optional[date] = None
    notes: Optional[str] = None


class ExamResultCreate(ExamResultBase):
    pass


class ExamResultBulkCreate(BaseModel):
    items: list[ExamResultCreate] = Field(min_length=1)


class ExamResultUpdate(BaseModel):
    name: Optional[str] = None
    exam_type: Optional[ExamType] = None
    result: Optional[str] = None
    exam_date: Optional[date] = None
    notes: Optional[str] = None


class ExamResultResponse(ExamResultBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True