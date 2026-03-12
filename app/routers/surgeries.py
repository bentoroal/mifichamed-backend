from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.surgery import SurgeryCatalog
from app.schemas.surgery import SurgeryCatalogResponse

router = APIRouter(prefix="/surgeries", tags=["Surgeries"])


@router.get("/", response_model=List[SurgeryCatalogResponse])
def get_surgeries(db: Session = Depends(get_db)):
    """
    Devuelve todas las cirugías del catálogo.
    """
    return db.query(SurgeryCatalog).order_by(SurgeryCatalog.name).all()