from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SymptomCatalogBase(BaseModel):
    name: str
    is_custom: Optional[bool] = False


class SymptomCatalogCreate(BaseModel):
    name: str
    is_custom: Optional[bool] = False


class SymptomCatalogResponse(SymptomCatalogBase):
    id: int
    created_at: datetime
    created_by_user_id: Optional[int] = None

    class Config:
        from_attributes = True
