from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey, Text, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class UserSurgery(Base):
    __tablename__ = "user_surgeries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    surgery_id = Column(Integer, ForeignKey("surgeries_catalog.id"), nullable=False)
    user_condition_id = Column(Integer, ForeignKey("user_conditions.id"), nullable=True)

    surgery_date = Column(Date, nullable=True)

    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # relaciones
    user = relationship("User", back_populates="surgeries")
    surgery = relationship("SurgeryCatalog")
    user_condition = relationship("UserCondition", back_populates="surgeries")