from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL
#variable que inicia la coneccion con SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
#Crea sesion para interactuar con db
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Dependencia de FastApi
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
