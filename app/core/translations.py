"""
Traducciones centralizadas para valores de enumeraciones.
Mantiene sincronización con el frontend.
"""

# Traducciones de hábitos del perfil
HABIT_TRANSLATIONS = {
    "alcohol_consumption": {
        "none": "No",
        "social": "Socialmente",
        "regular": "Regular",
        "heavy": "Fuerte",
    },
    "smoking_habits": {
        "none": "No",
        "social": "Socialmente",
        "regular": "Regular",
        "heavy": "Fuerte",
    },
    "physical_activity": {
        "none": "Nada",
        "light": "Poco",
        "moderate": "Moderado",
        "intense": "Intenso",
    },
    "sex": {
        "male": "Masculino",
        "female": "Femenino",
        "other": "Otro",
    },
}

# Traducciones de estados
STATUS_TRANSLATIONS = {
    "active": "Activa",
    "chronic": "Crónica",
    "resolved": "Resuelta",
    "remission": "Remisión",
}

# Traducciones de estados de alergias
ALLERGY_STATUS_TRANSLATIONS = {
    "active": "Activa",
    "remission": "Remisión",
}


def translate_value(field_name: str, value: str | None) -> str | None:
    """
    Traduce un valor basado en el nombre del campo.
    
    Args:
        field_name: El nombre del campo (ej: 'alcohol_consumption', 'status')
        value: El valor a traducir (ej: 'none', 'active')
    
    Returns:
        El valor traducido al español, o el valor original si no tiene traducción
    """
    if not value:
        return value
    
    # Buscar en traducciones de hábitos
    if field_name in HABIT_TRANSLATIONS:
        return HABIT_TRANSLATIONS[field_name].get(value, value)
    
    # Buscar en traducciones de estados
    if field_name == "status":
        # Para condiciones
        if value in STATUS_TRANSLATIONS:
            return STATUS_TRANSLATIONS[value]
        # Para alergias
        if value in ALLERGY_STATUS_TRANSLATIONS:
            return ALLERGY_STATUS_TRANSLATIONS[value]
    
    return value


def get_label(field_name: str, value: str | None) -> str:
    """
    Obtiene etiqueta legible (traducida) para un valor.
    Si no existe traducción, devuelve el valor original.
    
    Args:
        field_name: El nombre del campo
        value: El valor del campo
        
    Returns:
        Etiqueta traducida o valor original si no hay traducción
    """
    return translate_value(field_name, value) or "-"
