from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ConditionCatalogBase(BaseModel):
    name: str
    is_custom: Optional[bool] = False


class ConditionCatalogCreate(BaseModel):
    name: str
    is_custom: Optional[bool] = False


class ConditionCatalogResponse(ConditionCatalogBase):
    id: int
    created_at: datetime
    created_by_user_id: Optional[int] = None

    class Config:
        from_attributes = True
