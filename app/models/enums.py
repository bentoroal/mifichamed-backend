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

