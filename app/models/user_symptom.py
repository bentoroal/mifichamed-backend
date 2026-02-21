from sqlalchemy import Column, Integer, Date, Boolean, DateTime, ForeignKey, Text
from datetime import datetime
from app.db.base import Base


class UserSymptom(Base):
    __tablename__ = "user_symptoms"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    symptom_id = Column(Integer, ForeignKey("symptoms_catalog.id"), nullable=False)

    start_date = Column(Date, nullable=True) # Fecha en la que el usuario comenzó a experimentar el síntoma
    severity = Column(Integer, nullable=True)  # Escala de 1-10
    is_current = Column(Boolean, default=True) # Indica si el síntoma sigue presente o ya se resolvió

    notes = Column(Text, nullable=True) # Notas adicionales del usuario sobre el síntoma, como desencadenantes, alivios, etc.

    linked_condition_id = Column(
        Integer,
        ForeignKey("user_conditions.id"),
        nullable=True
    )

    created_at = Column(DateTime, default=datetime.utcnow)