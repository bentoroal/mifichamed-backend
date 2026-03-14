#Este archivo se encarga de la Logica del negocio

from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password, verify_password
from fastapi import HTTPException

#Funcion para crear el usuario
def create_user(db: Session, email: str, password: str):

    existing = db.query(User).filter(User.email == email).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="El correo ya ha sido registrado en otra cuenta"
        )

    user = User(
        email=email,
        hashed_password=hash_password(password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
