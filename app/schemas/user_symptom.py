from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class SymptomSimple(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class UserSymptomBase(BaseModel):
    symptom_id: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    severity: Optional[int] = None
    is_current: Optional[bool] = True
    notes: Optional[str] = None


class UserSymptomCreate(UserSymptomBase):
    pass

class UserSymptomResponse(UserSymptomBase):
    id: int
    user_id: int
    created_at: datetime

    symptom: SymptomSimple

    class Config:
        from_attributes = True

class UserSymptomUpdate(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    severity: Optional[int] = None
    is_current: Optional[bool] = None
    notes: Optional[str] = None
