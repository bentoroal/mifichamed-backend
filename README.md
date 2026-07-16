````markdown
# MiFichaMed Backend

Backend de **MiFichaMed**, una API REST desarrollada con **FastAPI** para la gestión de fichas médicas personales. El sistema permite a cada usuario mantener un historial clínico digital con autenticación segura, administración de enfermedades, síntomas, tratamientos, alergias, cirugías, perfil médico e informes clínicos.

El proyecto sigue una arquitectura modular basada en routers, servicios, modelos y esquemas, facilitando su mantenimiento y escalabilidad.

---

# Características

- Autenticación mediante JWT.
- Registro e inicio de sesión de usuarios.
- Gestión del perfil clínico.
- Administración de enfermedades.
- Administración de síntomas.
- Registro diario de síntomas.
- Administración de tratamientos.
- Administración de alergias.
- Administración de cirugías.
- Dashboard con resumen clínico.
- Generación de informes médicos.
- API REST completamente desacoplada del frontend.
- Base de datos relacional mediante SQLAlchemy.
- Validación de datos utilizando Pydantic.

---

# Tecnologías

| Tecnología | Uso |
|------------|-----|
| Python | Lenguaje principal |
| FastAPI | Framework REST |
| SQLAlchemy | ORM |
| Pydantic | Validación de datos |
| PostgreSQL | Base de datos (producción) |
| SQLite | Desarrollo local |
| JWT | Autenticación |
| Alembic | Migraciones |
| Uvicorn | Servidor ASGI |
| Passlib / BCrypt | Hash de contraseñas |
| Python-Jose | Firma y validación de tokens |

---

# Arquitectura

El backend está organizado siguiendo una arquitectura por capas.

```
Cliente
      │
      ▼
 Routers (API)
      │
      ▼
 Services
      │
      ▼
 SQLAlchemy ORM
      │
      ▼
 Base de Datos
```

Cada módulo encapsula completamente su funcionalidad mediante:

- Router
- Servicio
- Modelo
- Schema
- Operaciones CRUD

Esto evita dependencias innecesarias entre módulos y facilita la incorporación de nuevas funcionalidades.

---

# Organización del proyecto

```
app/

├── auth/
│   ├── autenticación
│   ├── JWT
│   └── login/registro
│
├── dashboard/
│   └── resumen clínico
│
├── database/
│   └── conexión SQLAlchemy
│
├── models/
│   └── modelos ORM
│
├── schemas/
│   └── modelos Pydantic
│
├── services/
│   └── lógica de negocio
│
├── routers/
│   └── endpoints REST
│
├── utils/
│   └── utilidades
│
└── main.py
```

---

# Modelo funcional

El sistema gira alrededor del usuario autenticado.

Cada usuario puede registrar:

- Perfil personal
- Condiciones médicas
- Síntomas
- Historial diario de síntomas
- Tratamientos
- Alergias
- Cirugías

El Dashboard obtiene información agregada de estos módulos para entregar un resumen general del estado clínico.

---

# Autenticación

La autenticación utiliza **JWT Bearer Token**.

Flujo simplificado:

```
Registro

Usuario
    │
POST /auth/register
    │
Hash contraseña
    │
Guardar usuario
```

Posteriormente:

```
Login

Usuario
    │
POST /auth/login
    │
Verificación contraseña
    │
Generación JWT
    │
Access Token
```

Los endpoints protegidos requieren:

```
Authorization: Bearer <token>
```

El usuario autenticado es obtenido mediante dependencias de FastAPI.

---

# Base de datos

El proyecto utiliza SQLAlchemy como ORM.

Durante el desarrollo puede trabajar con SQLite y en producción con PostgreSQL mediante la variable:

```
DATABASE_URL
```

La separación ORM / Pydantic permite desacoplar completamente la representación interna de la API pública.

---

# Principales módulos

## Auth

Responsable de:

- Registro
- Login
- Hash de contraseñas
- Validación de credenciales
- Generación de JWT
- Validación del usuario autenticado

---

## User Profile

Administra la información médica básica del usuario, utilizada posteriormente por el Dashboard y los informes.

---

## Conditions

Permite administrar enfermedades o condiciones médicas del usuario.

Incluye:

- catálogo
- condiciones personalizadas
- estado
- fechas
- notas

---

## Symptoms

Gestiona los síntomas registrados por el usuario.

Incluye además el registro diario para llevar seguimiento de evolución.

---

## Treatments

Permite registrar tratamientos activos o históricos.

Incluye información como:

- medicamento
- dosis
- frecuencia
- fechas
- observaciones

---

## Allergies

Permite mantener un historial de alergias del paciente.

Puede utilizar tanto elementos del catálogo como registros personalizados.

---

## Surgeries

Administra intervenciones quirúrgicas realizadas al paciente.

Incluye fechas, observaciones e historial.

---

## Dashboard

Entrega una vista consolidada de la información clínica del usuario.

Agrupa información proveniente de los distintos módulos del sistema para facilitar la consulta rápida.

---

## Reports

Genera informes médicos a partir de la información registrada por el usuario.

Los reportes permiten incluir distintas secciones dependiendo de los filtros seleccionados.

---

# API REST

La aplicación expone endpoints REST organizados por módulos.

Ejemplos:

```
/auth

/user-profile

/dashboard

/conditions

/user-conditions

/symptoms

/user-symptoms

/treatments

/user-treatments

/allergies

/user-allergies

/surgeries

/user-surgeries

/report
```

La API utiliza principalmente los métodos:

- GET
- POST
- PATCH
- DELETE

---

# Flujo de una petición

```
Cliente

↓

Router

↓

Validación Pydantic

↓

Servicio

↓

SQLAlchemy

↓

Base de datos

↓

Respuesta JSON
```

---

# Variables de entorno

El proyecto utiliza variables de entorno para la configuración.

Entre ellas se encuentran:

```
DATABASE_URL

SECRET_KEY

ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES

REFRESH_TOKEN_EXPIRE_DAYS
```

Estas variables permiten cambiar fácilmente entre entornos de desarrollo y producción.

---

# Seguridad

El backend implementa distintas medidas de seguridad:

- Contraseñas hasheadas.
- JWT firmado.
- Endpoints protegidos.
- Validación de datos mediante Pydantic.
- Separación entre modelos internos y públicos.
- Acceso únicamente a la información del usuario autenticado.

---

# Instalación

```bash
git clone <repositorio>

cd backend

python -m venv .venv

source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Configurar el archivo `.env`.

Ejecutar:

```bash
uvicorn app.main:app --reload
```

---

# Principios de diseño

El proyecto busca mantener:

- Arquitectura modular.
- Separación de responsabilidades.
- Reutilización de servicios.
- Escalabilidad.
- Código mantenible.
- API desacoplada del frontend.

---

# Estado del proyecto

Actualmente el backend proporciona una API REST para la administración de información clínica personal, incluyendo autenticación, historial médico, seguimiento de síntomas, tratamientos, alergias, cirugías, perfil del paciente y generación de informes, constituyendo el núcleo de la plataforma MiFichaMed.
````
