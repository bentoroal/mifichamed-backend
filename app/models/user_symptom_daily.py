from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class UserSymptomDaily(Base):
    __tablename__ = "user_symptoms_daily"

    id = Column(Integer, primary_key=True, index=True)

    user_symptom_id = Column(Integer, ForeignKey("user_symptoms.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)  # Fecha del registro de intensidad
    
    severity = Column(Integer, nullable=False)  # Escala de 1-10 para ese día específico
    notes = Column(Text, nullable=True)  # Notas específicas de ese día
    
    recorded_at = Column(DateTime, default=datetime.utcnow)

    # Relación para conectar con el síntoma del usuario
    user_symptom = relationship("UserSymptom", back_populates="daily_records")
