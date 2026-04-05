#Este archivo crea la app, las tablas, rutas y endpoint raiz
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import Base
from app.db.session import engine
from app.routers import auth, conditions, medications, symptoms, user_conditions, user_symptoms, user_symptom_daily, condition_treatments, dashboard, user_profile, user_surgeries, user_allergies, allergies, surgeries

import app.models  # imported so that SQLAlchemy model classes are registered, unused variable

#crea las tablas
Base.metadata.create_all(bind=engine)

#Crea la App
app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
app.include_router(user_symptom_daily.router)
app.include_router(condition_treatments.router)
app.include_router(dashboard.router)
app.include_router(user_profile.router)
app.include_router(user_surgeries.router)
app.include_router(user_allergies.router)
app.include_router(allergies.router)
app.include_router(surgeries.router)

#Crea el endpoint raiz
@app.get("/")
def root():
    return {"message": "MiFichaMed API running"}
