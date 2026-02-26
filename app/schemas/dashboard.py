from pydantic import BaseModel
from typing import List, Optional
from app.schemas.user_profile import UserProfileOut

class MedicationOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class TreatmentOut(BaseModel):
    id: int
    dosage: Optional[str]
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


class DashboardOut(BaseModel):
    profile: UserProfileOut | None
    active_conditions: list[UserConditionOut]
    active_symptoms: list[UserSymptomOut]

    class Config:
        from_attributes = True