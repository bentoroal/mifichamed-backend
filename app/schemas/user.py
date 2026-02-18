#Los schemas es el "modelo" pero en la perspectiva de la api, no de la db
#Este archivo Define cómo la API recibe y devuelve datos.
from pydantic import BaseModel, EmailStr

#Datos al crear usuario
class UserCreate(BaseModel):
    email: EmailStr
    password: str

#Datos al hacer login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

#Datos que se retornan, nunca se retorna clave obviamente
class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
        
#Datos del token de acceso
class Token(BaseModel):
    access_token: str
    token_type: str

