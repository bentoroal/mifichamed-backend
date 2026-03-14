from sqlalchemy.orm import Session, joinedload
from app.models import User
from app.models.user_condition import UserCondition
from app.models.condition_treatment import ConditionTreatment
from app.models.user_symptom import UserSymptom
from app.models.user_profile import UserProfile
from app.models.user_allergy import UserAllergy
from app.models.enums import ConditionStatus, AllergyStatus
from datetime import date

def get_dashboard(db: Session, user_id: int):

    # Perfil
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    active_conditions = (
        db.query(UserCondition)
        .options(
            joinedload(UserCondition.condition),
            joinedload(UserCondition.treatments)
                .joinedload(ConditionTreatment.medication)
        )
        .filter(
            UserCondition.user_id == user_id,
            UserCondition.status == ConditionStatus.ACTIVE
        )
        .all()
    )

    # Filtrar tratamientos activos (fecha)
    today = date.today()
    for condition in active_conditions:
        condition.treatments = [
            t for t in condition.treatments
            if t.end_date is None or t.end_date >= today
        ]

    active_symptoms = (
        db.query(UserSymptom)
        .options(joinedload(UserSymptom.symptom))
        .filter(
            UserSymptom.user_id == user_id,
            UserSymptom.is_current == True
        )
        .all()
    )

    active_allergies = (
        db.query(UserAllergy)
        .options(joinedload(UserAllergy.allergy))
        .filter(
            UserAllergy.user_id == user_id,
            UserAllergy.status == AllergyStatus.ACTIVE
        )
        .all()
    )
    active_allergies = [
        a for a in active_allergies
        if a.end_date is None or a.end_date >= today
    ]

    counts = {
        "conditions": len(active_conditions),
        "symptoms": len(active_symptoms),
        "allergies": len(active_allergies),
    }
    
    return {
        "profile": profile,
        "active_conditions": active_conditions,
        "active_symptoms": active_symptoms,
        "active_allergies": active_allergies,
        "counts": counts
    }