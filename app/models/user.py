#Creamos modelo de usuario con sus atributos
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    #Relaciones se usan para acceder a las condiciones médicas y tratamientos asociados a un usuario
    conditions = relationship("UserCondition", back_populates="user", cascade="all, delete")
    symptoms = relationship("UserSymptom", back_populates="user", cascade="all, delete")
    surgeries = relationship("UserSurgery", back_populates="user", cascade="all, delete")
    allergies = relationship("UserAllergy", back_populates="user", cascade="all, delete")
    profile = relationship("UserProfile", back_populates="user", uselist=False)
