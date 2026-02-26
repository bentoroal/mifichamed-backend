from pydantic import BaseModel
from datetime import date
from typing import Optional


class UserProfileBase(BaseModel):
    full_name: str
    birth_date: Optional[date] = None
    sex: Optional[str] = None


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    birth_date: Optional[date] = None
    sex: Optional[str] = None


class UserProfileOut(UserProfileBase):
    id: int

    class Config:
        from_attributes = True