from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey, Text, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base
from app.models.enums import AllergyStatus


class UserAllergy(Base):
    __tablename__ = "user_allergies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    allergy_id = Column(Integer, ForeignKey("allergies_catalog.id"), nullable=False)

    status = Column(SAEnum(AllergyStatus), default=AllergyStatus.ACTIVE, nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # relaciones
    user = relationship("User", back_populates="allergies")
    allergy = relationship("AllergyCatalog")