from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    full_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=True)
    sex = Column(String, nullable=True)
    weight = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)

    user = relationship("User", back_populates="profile")