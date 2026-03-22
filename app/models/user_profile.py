from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.enums import SexEnum


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    full_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=True)
    sex = Column(SqlEnum(SexEnum, name="sex_enum"), nullable=True)
    weight = Column(Float, nullable=True)
    height = Column(Integer, nullable=True)

    user = relationship("User", back_populates="profile")