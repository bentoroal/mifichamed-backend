from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class UserSymptomDailyBase(BaseModel):
    date: date
    severity: int  # Requerido: escala de 1-10
    notes: Optional[str] = None


class UserSymptomDailyCreate(UserSymptomDailyBase):
    pass


class UserSymptomDailyUpdate(BaseModel):
    severity: Optional[int] = None
    notes: Optional[str] = None


class UserSymptomDailyResponse(UserSymptomDailyBase):
    id: int
    user_symptom_id: int
    recorded_at: datetime

    class Config:
        from_attributes = True
