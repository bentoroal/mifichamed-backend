from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class ConditionTreatment(Base):
    __tablename__ = "condition_treatments"

    id = Column(Integer, primary_key=True, index=True)

    user_condition_id = Column(
        Integer,
        ForeignKey("user_conditions.id"),
        nullable=False
    )

    medication_id = Column(
        Integer,
        ForeignKey("medications_catalog.id"),
        nullable=True
    )

    dosage = Column(String, nullable=True)
    frequency = Column(String, nullable=True)

    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    #Relaciones para conectar con la condición médica asociada a este tratamiento y el medicamento utilizado en el tratamiento
    user_condition = relationship("UserCondition", back_populates="treatments")
    medication = relationship("MedicationCatalog")