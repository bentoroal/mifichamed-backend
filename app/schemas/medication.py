from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MedicationCatalogBase(BaseModel):
    name: str
    is_custom: Optional[bool] = False
    created_by_user_id: Optional[int] = None


class MedicationCatalogCreate(MedicationCatalogBase):
    pass


class MedicationCatalogResponse(MedicationCatalogBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
