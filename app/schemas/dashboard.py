from pydantic import BaseModel
from typing import List, Optional


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
    id: int
    email: str
    conditions: List[UserConditionOut]
    symptoms: List[UserSymptomOut]

    class Config:
        from_attributes = True