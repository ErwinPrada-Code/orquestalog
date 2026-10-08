# OrquestaLog

Sistema de orquestación logística multiempresa. Permite gestionar órdenes de transporte asignadas a flotas, rutas y centros de distribución, con autenticación por roles.

**Stack:** Angular 22 · FastAPI · PostgreSQL

## Estructura

```
.
├── app/                      # Backend FastAPI
│   ├── core/                 # Configuración, base de datos y seguridad (JWT, roles)
│   ├── models/               # Modelos SQLAlchemy
│   ├── schemas/              # Esquemas Pydantic
│   ├── crud/                 # Lógica de acceso a datos y reglas de negocio
│   ├── routers/              # Endpoints (auth, ordenes, catálogos)
│   └── main.py
├── seed.py                   # Crea tablas y datos iniciales
├── requirements.txt
├── .env.example
├── AGENTS.md                 # Instrucciones para agentes de IA
└── frontend-orquestalog/     # Frontend Angular
    └── src/app/
        ├── core/             # Servicios, guards, interceptor, modelos, config
        └── features/         # auth, dashboard, ordenes
```

## Requisitos

- Python 3.14 (versión con la que se generó `requirements.txt`)
- Node.js 22.22.3 o superior (requerido por Angular 22) y npm
- PostgreSQL en ejecución en el puerto 5432

## Puesta en marcha local

### 1. Base de datos

```bash
sudo -u postgres psql -c "CREATE DATABASE orquestalog;"
```

Por defecto se usa el usuario `postgres` con contraseña `postgres`. Si es distinto, ajústalo en el `.env`.

**Alternativa con Docker** (no hace falta instalar PostgreSQL; crea la base `orquestalog` automáticamente):

```bash
docker compose up -d db
```

### 2. Backend (puerto 8000)

Ejecutar siempre desde la raíz del proyecto:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # editar SECRET_KEY y DATABASE_URL si es necesario
python seed.py                # crea las tablas y los datos iniciales (se puede repetir sin error)
uvicorn app.main:app --reload
```

Documentación interactiva de la API: http://127.0.0.1:8000/docs

### 3. Frontend (puerto 4200)

```bash
cd frontend-orquestalog
npm install
npm start
```

Abrir http://localhost:4200. La URL de la API se configura en `frontend-orquestalog/src/app/core/config/api.ts`.

## Usuarios de prueba

| Rol | Correo | Contraseña |
|---|---|---|
| Administrador | admin@orquestalog.com | admin123 |
| Gestor logístico | gestor@orquestalog.com | gestor123 |
| Conductor | conductor@orquestalog.com | conductor123 |

## Roles y permisos

| Acción | Administrador | Gestor | Conductor |
|---|:---:|:---:|:---:|
| Ver órdenes, dashboard y catálogos | ✅ | ✅ | ✅ |
| Crear y editar órdenes | ✅ | ✅ | ❌ |
| Eliminar órdenes | ✅ | ❌ | ❌ |
| Gestionar flotas (crear, editar, eliminar) | ✅ | ❌ | ❌ |

Los permisos se validan en el backend (respuesta 403) y se reflejan en la interfaz.

## Endpoints principales

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/v1/auth/login` | Inicio de sesión, devuelve JWT |
| GET | `/api/v1/ordenes/` | Listar órdenes de la empresa |
| GET | `/api/v1/ordenes/resumen` | Totales por estado (dashboard) |
| GET | `/api/v1/ordenes/{id}` | Detalle de una orden |
| POST | `/api/v1/ordenes/` | Crear orden |
| PUT | `/api/v1/ordenes/{id}` | Actualizar orden |
| DELETE | `/api/v1/ordenes/{id}` | Eliminar orden |
| GET | `/api/v1/centros`, `/flotas`, `/rutas` | Catálogos para el formulario |
| GET / POST / PUT / DELETE | `/api/v1/flotas` y `/api/v1/flotas/{id}` | CRUD de flotas (escritura solo administrador) |

## Reglas de negocio

- **Aislamiento por empresa:** la empresa se toma del token JWT; cada usuario solo ve y modifica datos de su empresa.
- **Capacidad de flota:** una flota no puede tener más órdenes activas (`pendiente` o `en_proceso`) que su capacidad. Se valida al crear y al editar; una orden `completada` no consume capacidad.
- El centro, la ruta y la flota de una orden deben pertenecer a la misma empresa del usuario.
- **Capacidad al editar flotas:** no se puede reducir la capacidad de una flota por debajo de su número de órdenes activas.
- **Integridad al eliminar flotas:** no se puede eliminar una flota que tenga órdenes asociadas (respuesta 409).

## Pruebas

Backend (desde la raíz, con el entorno virtual activo; no requiere PostgreSQL):

```bash
python -m pytest
```

Cubren: hashing, JWT (inválido y vencido), respuestas 401 y 403 por rol, y las reglas de capacidad de flota.

Frontend:

```bash
cd frontend-orquestalog
npm test -- --watch=false
```