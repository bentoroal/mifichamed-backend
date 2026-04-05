from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey, Text, UniqueConstraint, Index, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class UserSymptomDaily(Base):
    __tablename__ = "user_symptoms_daily"


    __table_args__ = (
        UniqueConstraint("user_symptom_id", "date", name="uq_symptom_day"),
        Index("idx_user_symptom_date", "user_symptom_id", "date"),
        CheckConstraint("severity >= 1 AND severity <= 10", name="check_severity_range"),
    )

    id = Column(Integer, primary_key=True, index=True)

    user_symptom_id = Column(
        Integer,
        ForeignKey("user_symptoms.id", ondelete="CASCADE"),
        nullable=False
    )

    date = Column(
        Date,
        nullable=False
    )

    # 👉 escala 1-10
    severity = Column(
        Integer,
        nullable=False
    )

    notes = Column(Text, nullable=True)

    recorded_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # 🔗 relación
    user_symptom = relationship(
        "UserSymptom",
        back_populates="daily_records"
    )