from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class UserSurgeryBase(BaseModel):
    surgery_id: int
    user_condition_id: Optional[int] = None
    surgery_date: Optional[date] = None
    notes: Optional[str] = None

class UserSurgeryCreate(BaseModel):
    surgery_id: Optional[int] = None
    name: Optional[str] = None  # permite crear catálogo si no existe
    user_condition_id: Optional[int] = None
    surgery_date: Optional[date] = None
    notes: Optional[str] = None

class UserSurgeryUpdate(BaseModel):
    surgery_id: Optional[int] = None
    user_condition_id: Optional[int] = None
    surgery_date: Optional[date] = None
    notes: Optional[str] = None

class UserSurgeryResponse(UserSurgeryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True