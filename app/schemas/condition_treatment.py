from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class ConditionTreatmentBase(BaseModel):
    user_condition_id: int
    medication_id: Optional[int] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    notes: Optional[str] = None


class ConditionTreatmentCreate(ConditionTreatmentBase):
    pass


class ConditionTreatmentResponse(ConditionTreatmentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
