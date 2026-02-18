#Este archivo crea la app, las tablas, rutas y endpoint raiz
from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.routers import auth

#crea las tablas
Base.metadata.create_all(bind=engine)

#Crea la App
app = FastAPI()

#Registra Rutas
app.include_router(auth.router)

#Crea el endpoint raiz
@app.get("/")
def root():
    return {"message": "MiFichaMed API running"}
