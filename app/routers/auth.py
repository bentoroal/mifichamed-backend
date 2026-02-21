#Este archivo define las rutas de la api
from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, Token
from app.services.user_service import create_user, authenticate_user
from app.db.session import get_db
from app.core.security import create_access_token, get_current_user, create_refresh_token, verify_refresh_token
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])

#Ruta para crear nuevo usuario
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user.email, user.password)

#Ruta para logear usuario
@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = authenticate_user(db, form_data.username, form_data.password)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": db_user.email})
    refresh_token= create_refresh_token({"sub": db_user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

#Ruta para refrescar token de acceso usando el token de refresco
@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str = Body(...)):
    
    payload = verify_refresh_token(refresh_token)

    email = payload.get("sub")

    new_access_token = create_access_token({"sub": email})

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }

#Ruta para obtener datos del usuario logeado, se protege con el token de acceso
@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

