from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.allergy import AllergyCatalog
from app.schemas.allergy import AllergyCatalogResponse

router = APIRouter(prefix="/allergies", tags=["Allergies"])


@router.get("/", response_model=List[AllergyCatalogResponse])
def get_allergies(db: Session = Depends(get_db)):
    """
    Devuelve todas las alergias del catálogo.
    Incluye alergias globales y personalizadas.
    """
    return db.query(AllergyCatalog).order_by(AllergyCatalog.name).all()