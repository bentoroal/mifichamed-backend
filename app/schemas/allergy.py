from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from app.models.enums import AllergyStatus


# catálogo de alergias
class AllergyCatalogBase(BaseModel):
    name: str


class AllergyCatalogCreate(AllergyCatalogBase):
    is_custom: Optional[bool] = False
    created_by_user_id: Optional[int] = None


class AllergyCatalogResponse(AllergyCatalogBase):
    id: int
    is_custom: bool
    created_by_user_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


# relación usuario - alergia
class UserAllergyBase(BaseModel):
    allergy_id: int
    status: Optional[AllergyStatus] = AllergyStatus.ACTIVE
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    notes: Optional[str] = None


class UserAllergyCreate(BaseModel):
    allergy_id: Optional[int] = None
    name: Optional[str] = None  # permitimos pasar nombre para crear catálogo si no existe
    status: Optional[AllergyStatus] = AllergyStatus.ACTIVE
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    notes: Optional[str] = None


class UserAllergyUpdate(BaseModel):
    allergy_id: Optional[int] = None
    status: Optional[AllergyStatus] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    notes: Optional[str] = None


class UserAllergyResponse(UserAllergyBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True