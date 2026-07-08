from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
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
    start_date: Optional[date]
    end_date: Optional[date]
    notes: Optional[str]
    medication: Optional[MedicationOut]

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
    start_date: Optional[date]
    end_date: Optional[date]
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
    start_date: Optional[date]
    end_date: Optional[date]
    severity: Optional[int]
    notes: Optional[str]
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
    notes: Optional[str]
    allergy: AllergyCatalogOut

    class Config:
        from_attributes = True


class SurgeryCatalogOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class UserSurgeryOut(BaseModel):
    id: int
    surgery_date: Optional[date]
    notes: Optional[str]
    surgery: SurgeryCatalogOut

    class Config:
        from_attributes = True


class ReportOut(BaseModel):
    generated_at: datetime
    detail: str
    included_sections: List[str]
    profile: UserProfileOut | None
    active_conditions: List[UserConditionOut]
    active_symptoms: List[UserSymptomOut]
    active_allergies: List[UserAllergyOut]
    surgeries: List[UserSurgeryOut]

    class Config:
        from_attributes = True
