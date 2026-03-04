#Este archivo crea la app, las tablas, rutas y endpoint raiz
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import Base
from app.db.session import engine
from app.routers import auth, conditions, medications, symptoms, user_conditions, user_symptoms, condition_treatments, dashboard, user_profile

import app.models

#crea las tablas
Base.metadata.create_all(bind=engine)

#Crea la App
app = FastAPI()

origins = [
    "http://localhost:3000",  # tu frontend en local
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # puedes poner ["*"] para pruebas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Registra Rutas
app.include_router(auth.router)
app.include_router(conditions.router)
app.include_router(medications.router)
app.include_router(symptoms.router)
app.include_router(user_conditions.router)
app.include_router(user_symptoms.router)
app.include_router(condition_treatments.router)
app.include_router(dashboard.router)
app.include_router(user_profile.router)

#Crea el endpoint raiz
@app.get("/")
def root():
    return {"message": "MiFichaMed API running"}
