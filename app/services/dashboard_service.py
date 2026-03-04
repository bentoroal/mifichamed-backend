from sqlalchemy.orm import Session, joinedload
from app.models import User
from app.models.user_condition import UserCondition
from app.models.condition_treatment import ConditionTreatment
from app.models.user_symptom import UserSymptom
from app.models.user_profile import UserProfile
from app.models.enums import ConditionStatus
from datetime import date

def get_dashboard(db: Session, user_id: int):

    # Perfil
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    #Condiciones activas
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

    # Filtrar tratamientos activos manualmente
    today = date.today()
    for condition in active_conditions:
        condition.treatments = [
            t for t in condition.treatments
            if t.end_date is None or t.end_date >= today
        ]

    # Síntomas actuales
    active_symptoms = (
        db.query(UserSymptom)
        .options(joinedload(UserSymptom.symptom))
        .filter(
            UserSymptom.user_id == user_id,
            UserSymptom.is_current == True
        )
        .all()
    )

    return {
        "profile": profile,
        "active_conditions": active_conditions,
        "active_symptoms": active_symptoms
    }