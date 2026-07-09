from datetime import date, datetime

from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import or_

from app.models.condition_treatment import ConditionTreatment
from app.models.enums import AllergyStatus, ConditionStatus
from app.models.user_allergy import UserAllergy
from app.models.user_condition import UserCondition
from app.models.user_profile import UserProfile
from app.models.user_surgery import UserSurgery
from app.models.user_symptom import UserSymptom


DEFAULT_REPORT_SECTIONS = {
    "profile",
    "conditions",
    "treatments",
    "symptoms",
    "allergies",
}

AVAILABLE_REPORT_SECTIONS = DEFAULT_REPORT_SECTIONS | {
    "surgeries",
}


def _normalize_sections(sections: list[str] | None) -> set[str]:
    if not sections:
        return set(DEFAULT_REPORT_SECTIONS)

    normalized = {section.strip().lower() for section in sections if section.strip()}
    selected_sections = normalized & AVAILABLE_REPORT_SECTIONS

    if "treatments" in selected_sections:
        selected_sections.add("conditions")

    return selected_sections


def _serialize_treatment(treatment: ConditionTreatment) -> dict:
    return {
        "id": treatment.id,
        "dosage": treatment.dosage,
        "frequency": treatment.frequency,
        "start_date": treatment.start_date,
        "end_date": treatment.end_date,
        "notes": treatment.notes,
        "medication": (
            {
                "id": treatment.medication.id,
                "name": treatment.medication.name,
            }
            if treatment.medication
            else None
        ),
    }


def _serialize_condition(
    condition: UserCondition,
    treatments: list[ConditionTreatment],
    include_treatments: bool,
) -> dict:
    return {
        "id": condition.id,
        "status": condition.status,
        "start_date": condition.start_date,
        "end_date": condition.end_date,
        "notes": condition.notes,
        "condition": {
            "id": condition.condition.id,
            "name": condition.condition.name,
        },
        "treatments": (
            [_serialize_treatment(treatment) for treatment in treatments]
            if include_treatments
            else []
        ),
    }


def _serialize_symptom(symptom: UserSymptom) -> dict:
    return {
        "id": symptom.id,
        "start_date": symptom.start_date,
        "end_date": symptom.end_date,
        "severity": symptom.severity,
        "notes": symptom.notes,
        "symptom": {
            "id": symptom.symptom.id,
            "name": symptom.symptom.name,
        },
    }


def _serialize_allergy(allergy: UserAllergy) -> dict:
    return {
        "id": allergy.id,
        "status": allergy.status,
        "start_date": allergy.start_date,
        "notes": allergy.notes,
        "allergy": {
            "id": allergy.allergy.id,
            "name": allergy.allergy.name,
        },
    }


def _serialize_surgery(surgery: UserSurgery) -> dict:
    return {
        "id": surgery.id,
        "surgery_date": surgery.surgery_date,
        "notes": surgery.notes,
        "surgery": {
            "id": surgery.surgery.id,
            "name": surgery.surgery.name,
        },
    }


def get_report(
    db: Session,
    user_id: int,
    sections: list[str] | None = None,
):
    selected_sections = _normalize_sections(sections)

    profile = None
    if "profile" in selected_sections:
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    active_conditions = (
        db.query(UserCondition)
        .options(
            joinedload(UserCondition.condition),
            joinedload(UserCondition.treatments).joinedload(
                ConditionTreatment.medication
            ),
        )
        .filter(
            UserCondition.user_id == user_id,
            or_(
                UserCondition.status == ConditionStatus.ACTIVE,
                UserCondition.status == ConditionStatus.CHRONIC,
            ),
        )
        .all()
        if "conditions" in selected_sections
        else []
    )

    today = date.today()
    active_conditions_out = []
    for condition in active_conditions:
        active_treatments = [
            treatment
            for treatment in condition.treatments
            if treatment.end_date is None or treatment.end_date >= today
        ]
        active_conditions_out.append(
            _serialize_condition(
                condition,
                active_treatments,
                "treatments" in selected_sections,
            )
        )

    active_symptoms = (
        [
            _serialize_symptom(symptom)
            for symptom in (
                db.query(UserSymptom)
                .options(joinedload(UserSymptom.symptom))
                .filter(
                    UserSymptom.user_id == user_id,
                    UserSymptom.is_current == True,
                )
                .all()
            )
        ]
        if "symptoms" in selected_sections
        else []
    )

    active_allergies = (
        [
            _serialize_allergy(allergy)
            for allergy in (
                db.query(UserAllergy)
                .options(joinedload(UserAllergy.allergy))
                .filter(
                    UserAllergy.user_id == user_id,
                    UserAllergy.status == AllergyStatus.ACTIVE,
                )
                .all()
            )
        ]
        if "allergies" in selected_sections
        else []
    )

    surgeries = (
        [
            _serialize_surgery(surgery)
            for surgery in (
                db.query(UserSurgery)
                .options(joinedload(UserSurgery.surgery))
                .filter(UserSurgery.user_id == user_id)
                .order_by(UserSurgery.surgery_date.desc())
                .all()
            )
        ]
        if "surgeries" in selected_sections
        else []
    )

    return {
        "generated_at": datetime.utcnow(),
        "included_sections": sorted(selected_sections),
        "profile": profile,
        "active_conditions": active_conditions_out,
        "active_symptoms": active_symptoms,
        "active_allergies": active_allergies,
        "surgeries": surgeries,
    }
