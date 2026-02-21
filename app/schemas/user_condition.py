from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class UserConditionBase(BaseModel):
    user_id: int
    condition_id: int
    diagnosis_date: Optional[date] = None
    status: Optional[str] = "active"
    notes: Optional[str] = None


class UserConditionCreate(UserConditionBase):
    pass


class UserConditionResponse(UserConditionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
