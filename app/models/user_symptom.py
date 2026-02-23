from sqlalchemy import Column, Integer, Date, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
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

    #Relaciones para conectar con el usuario que experimenta el síntoma, el síntoma específico del catálogo de síntomas y la condición médica asociada a este síntoma (si existe) para ayudar a identificar posibles relaciones entre síntomas y condiciones médicas. Esto también permite acceder fácilmente a los datos relacionados al consultar los síntomas de un usuario o las condiciones médicas asociadas a un síntoma específico.
    user = relationship("User", back_populates="symptoms")
    symptom = relationship("SymptomCatalog")
    linked_condition = relationship("UserCondition", back_populates="symptoms")