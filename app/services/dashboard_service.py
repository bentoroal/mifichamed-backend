from sqlalchemy.orm import Session, joinedload
from app.models.user import User
from app.models.user_condition import UserCondition
from app.models.condition_treatment import ConditionTreatment
from app.models.user_symptom import UserSymptom

def get_dashboard(db: Session, user_id: int):
    user = (
        db.query(User)
        .options(
            joinedload(User.conditions)
                .joinedload(UserCondition.condition),

            joinedload(User.conditions)
                .joinedload(UserCondition.treatments)
                .joinedload(ConditionTreatment.medication),

            joinedload(User.symptoms)
                .joinedload(UserSymptom.symptom)
        )
        .filter(User.id == user_id)
        .first()
    )

    return user