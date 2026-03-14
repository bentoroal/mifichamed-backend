from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from app.schemas.user_profile import UserProfileOut


class MedicationOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class TreatmentOut(BaseModel):
    id: int
    dosage: Optional[str]
    frequency: Optional[str]
    medication: MedicationOut

    class Config:
        from_attributes = True


class ConditionCatalogOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class UserConditionOut(BaseModel):
    id: int
    status: str
    notes: Optional[str]
    condition: ConditionCatalogOut
    treatments: List[TreatmentOut]

    class Config:
        from_attributes = True


class SymptomCatalogOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class UserSymptomOut(BaseModel):
    id: int
    severity: Optional[int]
    symptom: SymptomCatalogOut

    class Config:
        from_attributes = True


class AllergyCatalogOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class UserAllergyOut(BaseModel):
    id: int
    status: str
    start_date: Optional[date]
    end_date: Optional[date]
    notes: Optional[str]
    allergy: AllergyCatalogOut

    class Config:
        from_attributes = True


class DashboardOut(BaseModel):
    profile: UserProfileOut | None
    active_conditions: List[UserConditionOut]
    active_symptoms: List[UserSymptomOut]
    active_allergies: List[UserAllergyOut]

    class Config:
        from_attributes = True