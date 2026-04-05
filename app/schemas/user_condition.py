from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from app.models.enums import ConditionStatus
from app.schemas.condition import ConditionCatalogResponse


class UserConditionBase(BaseModel):
    condition_id: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[ConditionStatus] = ConditionStatus.ACTIVE
    notes: Optional[str] = None


class UserConditionCreate(UserConditionBase):
    pass


class UserConditionResponse(UserConditionBase):
    id: int
    created_at: datetime

    condition: ConditionCatalogResponse 

    class Config:
        from_attributes = True