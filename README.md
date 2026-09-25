# MiFichaMed Backend

API REST de **MiFichaMed** para gestionar la ficha médica personal de cada usuario. El backend está construido con FastAPI, SQLAlchemy y Pydantic, y ofrece autenticación JWT, historial clínico, resultados de exámenes, seguimiento de síntomas, tratamientos, alergias, cirugías, dashboard e informes.

## Contenido

- [Tecnologías y estructura](#tecnologías-y-estructura)
- [Puesta en marcha](#puesta-en-marcha)
- [Configuración](#configuración)
- [Arquitectura](#arquitectura)
- [Modelo de datos](#modelo-de-datos)
- [Autenticación](#autenticación)
- [API](#api)
- [Códigos de respuesta](#códigos-de-respuesta)

## Tecnologías y estructura

| Tecnología | Uso |
| --- | --- |
| Python | Lenguaje de programación |
| FastAPI | Framework HTTP y documentación OpenAPI |
| SQLAlchemy | ORM y definición de tablas |
| Pydantic | Validación de peticiones y respuestas |
| Uvicorn | Servidor ASGI |
| PostgreSQL o SQLite | Base de datos, según `DATABASE_URL` |
| Passlib con BCrypt | Hash y verificación de contraseñas |
| python-jose | Firma y validación de JWT |
| ReportLab | Generación opcional de informes PDF |

```text
app/
├── main.py                 # Crea la aplicación, tablas y registra routers
├── core/                   # Configuración, seguridad y traducciones
├── db/                     # Base declarativa y sesiones SQLAlchemy
├── models/                 # Tablas ORM y enums
├── schemas/                # Contratos Pydantic de entrada y salida
├── services/               # Lógica de negocio y acceso a datos
└── routers/                # Endpoints HTTP agrupados por funcionalidad
```

La aplicación importa `app.models` para registrar todos los modelos y ejecuta `Base.metadata.create_all(bind=engine)` al importar `app.main`. Esto crea las tablas que no existan; el proyecto no contiene actualmente una configuración de migraciones Alembic activa.

## Puesta en marcha

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Linux/macOS

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

La API queda disponible normalmente en `http://127.0.0.1:8000`. FastAPI publica además:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Configuración

Crear un archivo `.env` en la raíz del backend:

```env
DATABASE_URL=sqlite:///./mifichamed.db
SECRET_KEY=cambiar-por-una-clave-secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

Para PostgreSQL, sustituir `DATABASE_URL` por la cadena de conexión correspondiente, por ejemplo `postgresql+psycopg2://usuario:password@host:5432/basedatos`.

La configuración se carga en `app/core/config.py` mediante `python-dotenv`. `DATABASE_URL` es obligatoria; los valores numéricos de expiración también deben estar definidos.

## Arquitectura

```text
Cliente HTTP
    │
    ▼
Routers FastAPI
    │  validación Pydantic + dependencias
    ▼
Services
    │
    ▼
SQLAlchemy / SessionLocal
    │
    ▼
Base de datos
```

Cada petición protegida obtiene el usuario mediante `get_current_user`. Los servicios reciben la sesión y el `current_user.id`, de forma que las operaciones de historial se limitan al propietario autenticado.

## Modelo de datos

### Tablas

Las siguientes son las tablas declaradas por los modelos SQLAlchemy.

#### `users`

| Columna | Tipo | Detalles |
| --- | --- | --- |
| `id` | Integer | PK |
| `email` | String | Único e indexado |
| `hashed_password` | String | Contraseña almacenada con hash BCrypt |

Relaciones: un usuario puede tener un `user_profiles`, muchas condiciones, síntomas, alergias y cirugías.

#### `user_profiles`

| Columna | Tipo | Detalles |
| --- | --- | --- |
| `id` | Integer | PK |
| `user_id` | Integer | FK a `users.id`, único |
| `full_name` | String | Obligatorio |
| `birth_date` | Date | Opcional |
| `sex` | Enum | `male`, `female`, `other` |
| `weight` | Float | Opcional |
| `height` | Integer | Opcional |
| `alcohol_consumption` | Enum | `none`, `social`, `regular`, `heavy` |
| `smoking_habits` | Enum | `none`, `social`, `regular`, `heavy` |
| `physical_activity` | Enum | `none`, `light`, `moderate`, `intense` |

#### Catálogos

Las tablas de catálogo permiten reutilizar datos comunes y también registrar elementos personalizados por usuario. Comparten estas columnas:

| Tabla | Columnas específicas |
| --- | --- |
| `conditions_catalog` | `id`, `name`, `category`, `is_custom`, `created_by_user_id`, `created_at` |
| `symptoms_catalog` | `id`, `name`, `is_custom`, `created_by_user_id`, `created_at` |
| `medications_catalog` | `id`, `name`, `is_custom`, `created_by_user_id`, `created_at` |
| `allergies_catalog` | `id`, `name`, `is_custom`, `created_by_user_id`, `created_at` |
| `surgeries_catalog` | `id`, `name`, `is_custom`, `created_by_user_id`, `created_at` |

En todos los catálogos, `id` es PK, `name` es obligatorio e indexado, `is_custom` indica si es un registro personalizado y `created_by_user_id` es una FK nullable a `users.id`.

#### Historial del usuario

| Tabla | Columnas |
| --- | --- |
| `user_conditions` | `id` PK, `user_id` FK, `condition_id` FK, `start_date`, `end_date`, `status`, `notes`, `created_at` |
| `user_symptoms` | `id` PK, `user_id` FK, `symptom_id` FK, `start_date`, `end_date`, `severity`, `is_current`, `notes`, `created_at` |
| `user_allergies` | `id` PK, `user_id` FK, `allergy_id` FK, `status`, `start_date`, `notes`, `created_at` |
| `user_surgeries` | `id` PK, `user_id` FK, `surgery_id` FK, `user_condition_id` nullable FK, `surgery_date`, `notes`, `created_at` |
| `condition_treatments` | `id` PK, `user_condition_id` FK, `medication_id` nullable FK, `dosage`, `frequency`, `start_date`, `end_date`, `notes`, `created_at` |
| `user_symptoms_daily` | `id` PK, `user_symptom_id` FK, `date`, `severity`, `notes`, `recorded_at` |
| `exam_results` | `id` PK, `user_id` FK, `name`, `exam_type`, `result`, `exam_date`, `notes`, `created_at` |

`user_symptoms_daily` impone que no haya dos registros para el mismo síntoma y fecha (`user_symptom_id`, `date`), indexa esa combinación y limita `severity` al rango 1-10.

### Relaciones

```mermaid
erDiagram
    users ||--o| user_profiles : tiene
    users ||--o{ user_conditions : registra
    users ||--o{ user_symptoms : registra
    users ||--o{ user_allergies : registra
    users ||--o{ user_surgeries : registra
    users ||--o{ exam_results : registra
    conditions_catalog ||--o{ user_conditions : clasifica
    symptoms_catalog ||--o{ user_symptoms : clasifica
    allergies_catalog ||--o{ user_allergies : clasifica
    surgeries_catalog ||--o{ user_surgeries : clasifica
    user_conditions ||--o{ condition_treatments : recibe
    medications_catalog ||--o{ condition_treatments : usa
    user_conditions ||--o{ user_surgeries : relaciona
    user_symptoms ||--o{ user_symptoms_daily : detalla
```

Relaciones de borrado relevantes definidas en ORM: al borrar un usuario se borran sus condiciones, síntomas, cirugías y alergias; al borrar una condición del usuario se borran sus tratamientos y cirugías relacionadas; al borrar un síntoma se borran sus registros diarios. El registro diario también declara `ON DELETE CASCADE` hacia `user_symptoms`.

### Enums principales

- `ConditionCategory`: `cardiovascular`, `respiratory`, `endocrine_metabolic`, `digestive`, `neurological`, `musculoskeletal`, `dermatological`, `immune_allergic`, `mental_health`, `genitourinary`, `oncological`, `infectious`, `sensory`.
- `ConditionStatus`: `active`, `chronic`, `resolved`, `remission`.
- `AllergyStatus`: `active`, `remission`.
- `ExamType`: `blood`, `urine`, `stool`, `imaging`, `procedure`, `pathology`, `other`.
- Perfil: `SexEnum`, `AlcoholEnum`, `SmokingEnum`, `PhysicalActivityEnum`.

## Autenticación

Las rutas protegidas requieren:

```http
Authorization: Bearer <access_token>
```

1. `POST /auth/register` crea el usuario y almacena la contraseña hasheada.
2. `POST /auth/login` recibe el formulario OAuth2 (`username` es el email y `password` la contraseña) y devuelve `access_token`, `refresh_token` y `token_type`.
3. `POST /auth/refresh` recibe un refresh token y devuelve un nuevo access token.
4. `GET /auth/me` devuelve el usuario autenticado.

El access token incluye `type=access` y el refresh token `type=refresh`; no son intercambiables.

## API

Salvo `/`, `/allergies/` y `/surgeries/`, las rutas de esta sección requieren autenticación Bearer. Los endpoints de listados que soportan paginación aceptan `skip` y `limit`, con valores predeterminados `0` y `100`.

### Sistema y autenticación

| Método | Ruta | Descripción | Auth |
| --- | --- | --- | --- |
| GET | `/` | Comprueba que la API está funcionando. | No |
| POST | `/auth/register` | Registra un usuario. Body: `email`, `password`. | No |
| POST | `/auth/login` | Inicia sesión con formulario OAuth2. | No |
| POST | `/auth/refresh` | Body JSON: `{"refresh_token": "..."}`. | No, usa refresh token |
| GET | `/auth/me` | Devuelve el usuario actual. | Sí |

### Perfil y dashboard

| Método | Ruta | Descripción |
| --- | --- | --- |
| GET | `/user-profile/` | Obtiene el perfil del usuario. |
| POST | `/user-profile/` | Crea el perfil. Body: `full_name` y campos opcionales del perfil. |
| PATCH | `/user-profile/` | Actualiza parcialmente el perfil. |
| DELETE | `/user-profile/` | Elimina el perfil. |
| GET | `/dashboard/` | Devuelve el resumen clínico agregado. |

### Catálogos

| Método | Ruta | Descripción |
| --- | --- | --- |
| GET | `/conditions/` | Lista condiciones; filtros `category` y `search`. |
| GET | `/conditions/categories` | Lista los valores de `ConditionCategory`. |
| GET | `/conditions/by-category` | Filtra por `category` y opcionalmente `search`. |
| POST | `/conditions/` | Crea una condición personalizada. Body: `name`, `category`. |
| GET | `/conditions/{condition_id}` | Obtiene una condición. |
| DELETE | `/conditions/{condition_id}` | Elimina una condición accesible por el usuario. |
| GET | `/medications/` | Lista medicamentos. |
| POST | `/medications/` | Crea un medicamento personalizado. Body: `name`, `is_custom`. |
| GET | `/medications/{medication_id}` | Obtiene un medicamento. |
| DELETE | `/medications/{medication_id}` | Elimina un medicamento accesible por el usuario. |
| GET | `/symptoms/` | Lista síntomas. |
| POST | `/symptoms/` | Crea un síntoma personalizado. Body: `name`, `is_custom`. |
| GET | `/symptoms/{symptom_id}` | Obtiene un síntoma. |
| DELETE | `/symptoms/{symptom_id}` | Elimina un síntoma accesible por el usuario. |
| GET | `/allergies/` | Lista el catálogo de alergias. |
| GET | `/surgeries/` | Lista todas las cirugías del catálogo, sin paginación. |

### Historial clínico

| Método | Ruta | Descripción |
| --- | --- | --- |
| GET | `/user-conditions/` | Lista condiciones del usuario. |
| POST | `/user-conditions/` | Registra una condición. Body: `condition_id`, fechas, `status`, `notes`. |
| GET | `/user-conditions/{uc_id}` | Obtiene una condición registrada. |
| PATCH | `/user-conditions/{uc_id}` | Actualiza parcialmente una condición. |
| DELETE | `/user-conditions/{uc_id}` | Elimina una condición registrada. |
| GET | `/user-conditions/{uc_id}/symptoms` | Lista síntomas cuyo periodo se solapa con la condición. |
| GET | `/user-symptoms/` | Lista síntomas del usuario. |
| POST | `/user-symptoms/` | Registra un síntoma. Body: `symptom_id`, fechas, `severity`, `is_current`, `notes`. |
| GET | `/user-symptoms/{us_id}` | Obtiene un síntoma registrado. |
| PATCH | `/user-symptoms/{us_id}` | Actualiza parcialmente un síntoma. |
| DELETE | `/user-symptoms/{us_id}` | Elimina un síntoma registrado. |
| GET | `/user-symptoms/{us_id}/daily/` | Lista el seguimiento diario del síntoma. |
| GET | `/user-symptoms/{us_id}/daily/by-date` | Obtiene el registro diario para `date=YYYY-MM-DD`. |
| POST | `/user-symptoms/{us_id}/daily/` | Crea o actualiza el registro diario. Body: `date`, `severity`, `notes`. |
| PATCH | `/user-symptoms/{us_id}/daily/{daily_id}` | Actualiza un registro diario. |
| DELETE | `/user-symptoms/{us_id}/daily/{daily_id}` | Elimina un registro diario. |
| GET | `/condition-treatments/` | Lista tratamientos del usuario. |
| POST | `/condition-treatments/` | Registra tratamiento. Body: `user_condition_id`, `medication_id`, dosis, frecuencia, fechas y notas. |
| GET | `/condition-treatments/{t_id}` | Obtiene un tratamiento. |
| PATCH | `/condition-treatments/{t_id}` | Actualiza parcialmente un tratamiento. |
| DELETE | `/condition-treatments/{t_id}` | Elimina un tratamiento. |
| GET | `/user-allergies/` | Lista alergias del usuario. |
| POST | `/user-allergies/` | Registra alergia por `allergy_id` o nombre, con estado, fecha y notas. |
| GET | `/user-allergies/{ua_id}` | Obtiene una alergia registrada. |
| PATCH | `/user-allergies/{ua_id}` | Actualiza parcialmente una alergia. |
| DELETE | `/user-allergies/{ua_id}` | Elimina una alergia registrada. |
| GET | `/user-surgeries/` | Lista cirugías; filtro opcional `condition_id`. |
| POST | `/user-surgeries/` | Registra cirugía por `surgery_id` o nombre, opcionalmente asociada a condición. |
| GET | `/user-surgeries/{us_id}` | Obtiene una cirugía registrada. |
| PATCH | `/user-surgeries/{us_id}` | Actualiza parcialmente una cirugía. |
| DELETE | `/user-surgeries/{us_id}` | Elimina una cirugía registrada. |

### Resultados de exámenes

Cada resultado pertenece al usuario autenticado. `name` permite registrar nombres específicos como `Hemograma`, `TSH` o `Ecografía abdominal`, mientras que `exam_type` utiliza un tipo predefinido.

| Método | Ruta | Descripción |
| --- | --- | --- |
| GET | `/exam-results/types` | Lista los tipos de examen disponibles. |
| GET | `/exam-results/` | Lista resultados; filtros opcionales `exam_type`, `search`, `skip` y `limit`. |
| POST | `/exam-results/` | Crea un resultado. Body: `name`, `exam_type`, `result`, `exam_date` y `notes`. |
| POST | `/exam-results/bulk` | Crea varios resultados en una sola transacción. Body: `items`, una lista de objetos con los mismos campos del endpoint individual. |
| GET | `/exam-results/{exam_result_id}` | Obtiene un resultado. |
| PATCH | `/exam-results/{exam_result_id}` | Actualiza parcialmente un resultado. |
| DELETE | `/exam-results/{exam_result_id}` | Elimina un resultado. |

Ejemplo de creación masiva:

```json
{
    "items": [
        {
            "name": "Hemograma",
            "exam_type": "blood",
            "result": "Hemoglobina: 14.2 g/dL",
            "exam_date": "2026-09-24",
            "notes": "Resultado normal"
        },
        {
            "name": "Examen de orina",
            "exam_type": "urine",
            "result": "Sin hallazgos relevantes"
        }
    ]
}
```

### Informes

| Método | Ruta | Descripción |
| --- | --- | --- |
| GET | `/reports/` | Devuelve el informe JSON. `sections` es una lista separada por comas: `profile,conditions,treatments,symptoms,allergies,surgeries`. Sin filtro devuelve todas las secciones. |
| POST | `/reports/preview/` | Genera una previsualización JSON. Body: flags `includeProfile`, `includeConditions`, `includeTreatments`, `includeSymptoms`, `includeAllergies`, `includeSurgeries`. |
| POST | `/reports/pdf/` | Genera y descarga `informe-medico.pdf` usando los mismos flags del preview. |

El informe puede contener perfil, condiciones, tratamientos, síntomas, alergias y cirugías. Los valores de enums se traducen para la salida del informe.

## Códigos de respuesta

- `200 OK`: lectura o actualización correcta.
- `200 OK`: también es la respuesta actual de las operaciones de creación, porque los routers no declaran `status_code=201`.
- `204 No Content`: eliminación correcta; las rutas no devuelven cuerpo aunque declaren un `response_model`.
- `401 Unauthorized`: credenciales, access token o refresh token inválidos.
- `403 Forbidden`: el recurso relacionado no pertenece al usuario autenticado.
- `404 Not Found`: recurso inexistente o no accesible para el usuario.
- `409 Conflict`: intento de crear un perfil que ya existe.
- `422 Unprocessable Entity`: body o parámetros que no cumplen el schema Pydantic.
- `500 Internal Server Error`: error interno; la generación PDF también devuelve este código si ReportLab no está instalado.

## Notas de seguridad y operación

- No guardar `SECRET_KEY`, contraseñas ni credenciales de base de datos en el repositorio.
- Usar HTTPS en producción para proteger los tokens Bearer.
- El acceso a los registros clínicos se filtra por el usuario autenticado en los servicios.
- La lista de orígenes CORS permitidos está definida en `app/main.py` y actualmente incluye localhost en el puerto 3000 y el frontend desplegado de MiFichaMed.
- Para cambios de esquema en producción conviene incorporar migraciones versionadas antes de depender de `create_all`.
