# AGENTS.md

Proyecto académico **OrquestaLog**: API FastAPI en la raíz + app Angular en `frontend-orquestalog/`. Código, nombres e interfaz en **español** → mantener ese idioma en código y mensajes nuevos.

> El `AGENTS.md` heredado de `/home/erwin/Documentos/` describe un vault de Obsidian (`MiBoveda/`) de otro proyecto: sus reglas de Inbox/PARA **no aplican** aquí.

## Estructura

- Raíz (no es repo git): `app/` (paquete FastAPI), `seed.py`, `.venv` (Python 3.14.7).
- `frontend-orquestalog/`: Angular 22 con su **propio** `.git` (sin commits aún; todo en staging), npm 11.
- No hay CI, Docker, pre-commit, `requirements.txt` ni `pyproject.toml`. Las dependencias existen **solo dentro de `.venv`** (fastapi, uvicorn, SQLAlchemy 2 async, asyncpg, python-jose, passlib, pydantic-settings). Si hay que reinstalar, partir de `pip freeze`.

## Comandos

Backend (siempre desde la raíz del proyecto: los imports son `app.*`):

```bash
.venv/bin/uvicorn app.main:app --reload   # API en :8000
.venv/bin/python seed.py                  # crea tablas + datos por defecto
```

Frontend (`cd frontend-orquestalog`):

```bash
npm start                      # ng serve en :4200
npm run build                  # verificado: compila
npm test -- --watch=false      # Vitest; sin la flag queda en watch
```

No hay tests de backend ni linters/typecheck de Python (ruff/black/mypy no existen). La única verificación útil es `npm run build` + `npm test -- --watch=false`.

## Backend — detalles no obvios

- Postgres obligatorio: `postgresql+asyncpg://postgres:postgres@localhost:5432/orquestalog` (default en `app/core/config.py`; lee `.env`, pero **no existe ninguno**). La BD `orquestalog` debe estar creada.
- Sin migraciones: `seed.py` hace `Base.metadata.create_all` e inserta filas con **id=1** (empresa, centro, flota, ruta) de las que depende el formulario Angular (envía `empresa_id: 1`, `flota_id: 1`, etc.). Ejecutarlo antes de crear órdenes.
- El proceso arranca aunque Postgres esté caído (conecta al primer query); los endpoints de datos fallan después.
- `create_async_engine(..., echo=True)` → log SQL gigante en consola: es esperado, no "arreglarlo".
- Auth JWT (HS256, secreto hardcodeado en `app/core/config.py`). `POST /api/v1/auth/login` en `app/main.py` valida credenciales hardcodeadas (admin por defecto para la sustentación) y devuelve `{access_token}`; `GET /api/v1/auth/dev-login` fue eliminado.
- RBAC en `app/routers/ordenes.py` con `role_required`: POST/PUT → `admin|gestor`, DELETE → `admin`. Los GET **no** validan auth (el comentario dice "autenticados" pero no hay `Depends`).
- Regla de negocio en `app/crud/crud_ordenes.py`: al crear una orden valida que la flota no supere su capacidad de órdenes activas (`pendiente`/`en_proceso`).
- CORS solo permite `localhost:4200`, `127.0.0.1:4200` y hosts sin puerto.
- El frontend llama siempre con **barra final** (`/api/v1/ordenes/`); es intencional.

## Frontend — detalles no obvios

- URL de la API hardcodeada en `src/app/core/services/orden.service.ts` (`http://127.0.0.1:8000`). No hay `environment.ts` ni proxy de dev-server.
- `OrdenService` lee el token de `localStorage` (lo escribe `LoginComponent` tras `POST /api/v1/auth/login`). Ruta por defecto `''` → `/login`. Hay **route guard** (`core/guards/auth.guard.ts`, `authGuard` en `app.routes.ts` en las 3 rutas `/ordenes*`): sin token → redirect a `/login`. **No hay interceptor**: un token vencido (expira en 24 h) deja pasar el guard y el backend responde 401 sin cerrar sesión.
- **Gotcha de change detection**: `app.config.ts` usa `provideHttpClient(withXhr())` **a propósito**. En Angular 22 el backend por defecto es `fetch` (el de Angular 18+), y `zone.js` 0.16 **no parchea `fetch`** → los callbacks HTTP no corren en NgZone y la vista no se actualiza (detalle se queda en "Cargando..." para siempre). No quitar `withXhr()` ni "modernizarlo" a fetch sin migrar todo a signals/zoneless. El `cdr.detectChanges()` que aparece en `listado-ordenes.component.ts` es un workaround previo: ahora redundante pero inofensivo, no duplicarlo en componentes nuevos.
- **Angular 22 genera archivos SIN sufijo `.component`** (`ng g component foo` → `foo.ts`, clase `Foo`). Este repo usa la convención contraria en código vivo: **renombrar a `foo.component.*` / `FooComponent`** tras generar, o los imports de `app.routes.ts` no coinciden.
- **Stubs/placeholder que no son el código real** (no editarlos): `app.ts`/`app.html`/`app.css` (placeholder de CLI; el raíz real es `app.component.*`, que es el que arranca `main.ts`), `features/ordenes/*/{formulario-orden,listado-ordenes}.{ts,html,css}` (los reales son los `*.component.*`) y `core/services/orden.ts` (`class Orden`).
- Por lo anterior, `app.spec.ts`, los specs de `features/` y `core/services/orden.spec.ts` prueban código muerto: tests verdes ≠ cobertura real del código que corre.
- Estilo: Prettier (printWidth 100, single quotes, parser `angular` para HTML) + `.editorconfig` (2 espacios). El repo **no** está formateado hoy (`npx prettier --check .` falla en ~17 archivos): no hacer un formateo masivo, solo formatear los archivos que se toquen.
