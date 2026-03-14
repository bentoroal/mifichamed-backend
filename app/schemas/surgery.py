from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

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

