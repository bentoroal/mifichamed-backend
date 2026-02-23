from sqlalchemy import Column, Integer, Date, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class UserCondition(Base):
    __tablename__ = "user_conditions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    condition_id = Column(Integer, ForeignKey("conditions_catalog.id"), nullable=False)

    diagnosis_date = Column(Date, nullable=True)

    status = Column(String, default="active")  # active, resolved, cronic
    notes = Column(Text, nullable=True) # notas adicionales del usuario sobre la condición

    created_at = Column(DateTime, default=datetime.utcnow)

    #Relaciones para acceder a los datos relacionados con el usuario, la condición y los tratamientos asociados a esta condición
    user = relationship("User", back_populates="conditions")
    condition = relationship("ConditionCatalog", back_populates="user_conditions")
    treatments = relationship("ConditionTreatment", back_populates="user_condition", cascade="all, delete")
    symptoms = relationship("UserSymptom", back_populates="linked_condition")
