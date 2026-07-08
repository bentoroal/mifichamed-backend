import enum

class ConditionCategory(str, enum.Enum):
    CARDIOVASCULAR = "cardiovascular"
    RESPIRATORY = "respiratory"
    ENDOCRINE_METABOLIC = "endocrine_metabolic"
    DIGESTIVE = "digestive"
    NEUROLOGICAL = "neurological"
    MUSCULOSKELETAL = "musculoskeletal"
    DERMATOLOGICAL = "dermatological"
    IMMUNE_ALLERGIC = "immune_allergic"
    MENTAL_HEALTH = "mental_health"
    GENITOURINARY = "genitourinary"
    ONCOLOGICAL = "oncological"
    INFECTIOUS = "infectious"
    SENSORY = "sensory"

class ConditionStatus(str, enum.Enum):
    ACTIVE = "active"
    CHRONIC = "chronic"
    RESOLVED = "resolved"
    REMISSION = "remission"


class AllergyStatus(str, enum.Enum):
    ACTIVE = "active"
    REMISSION = "remission"

class SexEnum(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class AlcoholEnum(str, enum.Enum):
    NONE = "none"
    SOCIAL = "social"
    REGULAR = "regular"
    HEAVY = "heavy"

class SmokingEnum(str, enum.Enum):
    NONE = "none"
    SOCIAL = "social"
    REGULAR = "regular"
    HEAVY = "heavy"

class PhysicalActivityEnum(str, enum.Enum):
    NONE = "none"
    LIGHT = "light"
    MODERATE = "moderate"
    INTENSE = "intense"

