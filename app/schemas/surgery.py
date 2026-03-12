# app/schemas/surgery.py
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from app.models.enums import SurgeryStatus

# catálogo de cirugías
class SurgeryCatalogBase(BaseModel):
    name: str

class SurgeryCatalogCreate(SurgeryCatalogBase):
    is_custom: Optional[bool] = False
    created_by_user_id: Optional[int] = None

class SurgeryCatalogResponse(SurgeryCatalogBase):
    id: int
    is_custom: bool
    created_by_user_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

# relación usuario - cirugía
class UserSurgeryBase(BaseModel):
    surgery_id: int
    user_condition_id: Optional[int] = None
    surgery_date: Optional[date] = None
    status: Optional[SurgeryStatus] = SurgeryStatus.COMPLETED
    notes: Optional[str] = None

class UserSurgeryCreate(BaseModel):
    surgery_id: Optional[int] = None
    name: Optional[str] = None  # permite crear catálogo si no existe
    user_condition_id: Optional[int] = None
    surgery_date: Optional[date] = None
    status: Optional[SurgeryStatus] = SurgeryStatus.COMPLETED
    notes: Optional[str] = None

class UserSurgeryUpdate(BaseModel):
    surgery_id: Optional[int] = None
    user_condition_id: Optional[int] = None
    surgery_date: Optional[date] = None
    status: Optional[SurgeryStatus] = None
    notes: Optional[str] = None

class UserSurgeryResponse(UserSurgeryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True