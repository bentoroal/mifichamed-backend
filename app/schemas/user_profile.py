from pydantic import BaseModel, computed_field
from datetime import date, datetime
from typing import Optional
from app.models.enums import SexEnum, AlcoholEnum, SmokingEnum, PhysicalActivityEnum


class UserProfileBase(BaseModel):
    full_name: str
    birth_date: Optional[date] = None
    sex: Optional[SexEnum] = None
    weight: Optional[float] = None
    height: Optional[int] = None
    alcohol_consumption: Optional[AlcoholEnum] = None
    smoking_habits: Optional[SmokingEnum] = None
    physical_activity: Optional[PhysicalActivityEnum] = None


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    birth_date: Optional[date] = None
    sex: Optional[SexEnum] = None
    weight: Optional[float] = None
    height: Optional[int] = None
    alcohol_consumption: Optional[AlcoholEnum] = None
    smoking_habits: Optional[SmokingEnum] = None
    physical_activity: Optional[PhysicalActivityEnum] = None


class UserProfileOut(BaseModel):
    full_name: str
    birth_date: date | None
    sex: str | None
    weight: float | None
    height: int | None
    alcohol_consumption: str | None
    smoking_habits: str | None
    physical_activity: str | None

    @computed_field
    @property
    def age(self) -> int | None:
        """Calcula la edad a partir de la fecha de nacimiento"""
        if not self.birth_date:
            return None
        
        today = datetime.now().date()
        age = today.year - self.birth_date.year
        
        # Ajustar la edad si el cumpleaños aún no ha ocurrido este año
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        
        return age

    class Config:
        from_attributes = True 