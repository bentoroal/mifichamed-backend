from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class UserSymptomBase(BaseModel):
    symptom_id: int
    start_date: Optional[date] = None
    severity: Optional[int] = None
    is_current: Optional[bool] = True
    notes: Optional[str] = None
    linked_condition_id: Optional[int] = None


class UserSymptomCreate(UserSymptomBase):
    pass

class UserSymptomResponse(UserSymptomBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserSymptomUpdate(BaseModel):
    start_date: Optional[date] = None
    severity: Optional[int] = None
    is_current: Optional[bool] = None
    notes: Optional[str] = None
