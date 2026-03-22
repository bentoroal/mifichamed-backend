from pydantic import BaseModel
from datetime import date
from typing import Optional
from app.models.enums import SexEnum


class UserProfileBase(BaseModel):
    full_name: str
    birth_date: Optional[date] = None
    sex: Optional[SexEnum] = None
    weight: Optional[float] = None
    height: Optional[int] = None


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    birth_date: Optional[date] = None
    sex: Optional[SexEnum] = None
    weight: Optional[float] = None
    height: Optional[int] = None


class UserProfileOut(BaseModel):
    full_name: str
    birth_date: date | None
    sex: str | None
    weight: float | None
    height: int | None

    class Config:
        from_attributes = True 