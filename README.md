# MiFichaMed Backend

## Descripción

MiFichaMed es una aplicación backend desarrollada con FastAPI para la gestión de información médica personal. Permite a los usuarios registrar y seguir sus condiciones médicas, síntomas, tratamientos, cirugías, alergias y más, proporcionando una ficha médica digital completa y personalizable.

## Características Principales

- **Autenticación y Autorización**: Sistema de login con JWT para usuarios registrados.
- **Gestión de Condiciones Médicas**: Catálogo de condiciones predefinidas y personalizadas por usuario.
- **Seguimiento de Síntomas**: Registro diario de intensidad de síntomas asociados a condiciones.
- **Tratamientos**: Asociación de medicamentos y tratamientos a condiciones específicas.
- **Cirugías**: Registro de cirugías realizadas, opcionalmente vinculadas a condiciones médicas.
- **Alergias**: Seguimiento de alergias con estado (activa o en remisión).
- **Perfil de Usuario**: Información básica del usuario.
- **Dashboard**: Resumen y estadísticas de la información médica del usuario.

## Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido para APIs REST.
- **SQLAlchemy**: ORM para interactuar con la base de datos.
- **SQLite**: Base de datos utilizada (configurable para otros motores).
- **Pydantic**: Validación de datos y serialización.
- **JWT**: Autenticación basada en tokens.
- **CORS**: Soporte para solicitudes desde el frontend.

## Requisitos del Sistema

- Python 3.8 o superior
- pip para gestión de dependencias
- Entorno virtual recomendado (venv)

## Instalación

1. **Clona el repositorio**:
   ```bash
   git clone <url-del-repositorio>
   cd mifichamed-backend
   ```

2. **Crea un entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura la base de datos**:
   - La aplicación crea automáticamente las tablas al iniciar.
   - Para desarrollo, se usa SQLite por defecto.

5. **Ejecuta la aplicación**:
   ```bash
   uvicorn app.main:app --reload
   ```

   La API estará disponible en `http://localhost:8000`.

## Uso

### Documentación de la API

Una vez ejecutada la aplicación, accede a `http://localhost:8000/docs` para ver la documentación interactiva generada por Swagger UI.

### Endpoints Principales

- **Autenticación**:
  - `POST /auth/login`: Iniciar sesión
  - `POST /auth/register`: Registrar nuevo usuario

- **Condiciones**:
  - `GET /conditions`: Listar condiciones disponibles
  - `POST /conditions`: Crear condición personalizada

- **Condiciones de Usuario**:
  - `GET /user-conditions`: Listar condiciones del usuario
  - `POST /user-conditions`: Agregar condición al perfil

- **Síntomas**:
  - `GET /user-symptoms`: Listar síntomas del usuario
  - `POST /user-symptoms`: Registrar nuevo síntoma

- **Tratamientos**:
  - `GET /condition-treatments`: Listar tratamientos
  - `POST /condition-treatments`: Crear tratamiento

- **Cirugías**:
  - `GET /user-surgeries`: Listar cirugías del usuario
  - `POST /user-surgeries`: Registrar cirugía

- **Alergias**:
  - `GET /user-allergies`: Listar alergias del usuario
  - `POST /user-allergies`: Registrar alergia

- **Perfil**:
  - `GET /user-profile`: Obtener perfil del usuario
  - `PUT /user-profile`: Actualizar perfil

- **Dashboard**:
  - `GET /dashboard`: Resumen estadístico

## Estructura del Proyecto

```
mifichamed-backend/
├── app/
│   ├── core/           # Configuración central (seguridad, configuración)
│   ├── db/             # Configuración de base de datos
│   ├── models/         # Modelos de SQLAlchemy
│   ├── routers/        # Endpoints de la API
│   ├── schemas/        # Esquemas Pydantic para validación
│   ├── services/       # Lógica de negocio
│   └── main.py         # Punto de entrada de la aplicación
├── requirements.txt    # Dependencias del proyecto
└── README.md          # Este archivo
```

## Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```
SECRET_KEY=tu_clave_secreta_aqui
DATABASE_URL=sqlite:///./mifichamed.db
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Base de Datos

Por defecto, usa SQLite. Para cambiar a PostgreSQL u otro motor:

1. Actualiza `DATABASE_URL` en la configuración.
2. Instala el driver correspondiente (ej: `psycopg2` para PostgreSQL).
3. Asegúrate de que las migraciones sean compatibles.

## Desarrollo

### Ejecutar Pruebas

```bash
pytest
```

### Formateo de Código

```bash
black .
isort .
```

### Linting

```bash
flake8 .
```

## Contribución

1. Fork el proyecto.
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`).
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`).
4. Push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

Para preguntas o soporte, contacta al equipo de desarrollo.

---

**Nota**: Este proyecto está en desarrollo activo. Las funcionalidades pueden cambiar sin previo aviso.</content>
<parameter name="filePath">c:\Users\bento\Desktop\Cosas\PROYECTOS IT\MiFichaMed\mifichamed-backend\README.md
