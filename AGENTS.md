# AGENTS.md

Proyecto académico **OrquestaLog**: API FastAPI en la raíz + app Angular en `frontend-orquestalog/`. Código, nombres e interfaz en **español** → mantener ese idioma en código y mensajes nuevos.

- `README.md` (raíz) ya documenta setup local, usuarios de prueba, tabla de roles y endpoints: **no duplicarlo aquí**; este archivo es solo para trampas no obvias.
- El `AGENTS.md` heredado de `/home/erwin/Documentos/` describe un vault de Obsidian (`MiBoveda/`) de otro proyecto: sus reglas de Inbox/PARA **no aplican** aquí.

## Estructura

- Raíz **sí es repo git** (un solo repo): `app/` (paquete FastAPI), `seed.py`, `.venv` (Python 3.14.7). `frontend-orquestalog/` está incluido en ese mismo repo (ya **no** tiene `.git` propio), npm 11.
- No hay CI, Docker, pre-commit ni `pyproject.toml`. Existe **`requirements.txt`** (generado con `pip freeze`, 28 paquetes, Python 3.14): para reinstalar, `python -m venv .venv && .venv/bin/pip install -r requirements.txt` y después regenerarlo con `.venv/bin/pip freeze > requirements.txt` si cambian las deps.
- Entorno: existe **`.env.example`** (DATABASE_URL, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES) y `.env` está en `.gitignore` → copiarlo con `cp .env.example .env`. `app/core/config.py` (pydantic-settings) lee `.env` **relativo a la raíz** (hay que arrancar el backend desde ahí); si no existe, manda los defaults hardcodeados (SECRET_KEY incluida).
- Hashing con **bcrypt directo** (`bcrypt.hashpw`/`checkpw` en `app/core/security.py`); **passlib fue retirado** porque es incompatible con bcrypt ≥ 4.1 (con bcrypt 5.0 `pwd_context.verify` lanzaba `ValueError`). No reinstalarlo.

## Comandos

Backend (siempre desde la raíz del proyecto: los imports son `app.*`):

```bash
.venv/bin/uvicorn app.main:app --reload   # API en :8000
.venv/bin/python seed.py                  # idempotente: tablas + datos + usuarios
```

Frontend (`cd frontend-orquestalog`):

```bash
npm start                      # ng serve en :4200
npm run build                  # verificado hoy: compila
npm test -- --watch=false      # Vitest; sin la flag queda en watch (5 archivos / 10 tests, todos verdes)
```

Hay tests de backend en `tests/` (pytest + httpx, sin necesidad de PostgreSQL): `python -m pytest` desde la raíz. Siguen sin existir linters/typecheck de Python. Verificación útil: `python -m pytest` + `npm run build` + `npm test -- --watch=false`. Dependencias nuevas: `pytest` y `httpx` (regenerar `requirements.txt` con `pip freeze`).

## Backend — detalles no obvios

- Postgres obligatorio: `postgresql+asyncpg://postgres:postgres@localhost:5432/orquestalog` (default en `app/core/config.py`; lee `.env`, pero puede no existir). La BD `orquestalog` debe estar creada.
- Sin migraciones: `seed.py` hace `Base.metadata.create_all` con `db.get` por id (se puede re-ejecutar sin error), crea empresa/centros/flotas/rutas con **ids fijos 1 y 2**, 3 usuarios con hash bcrypt (`admin@orquestalog.com`/`admin123`, `gestor@…`/`gestor123`, `conductor@…`/`conductor123`) y **reasigna las secuencias de id** con `setval` (los ids se insertaron a mano). Ejecutarlo antes de crear órdenes o loguearse.
- El proceso arranca aunque Postgres esté caído (conecta al primer query); los endpoints de datos fallan después.
- El log SQL está apagado por defecto: `echo=settings.DB_ECHO` (variable `DB_ECHO=true` en `.env` para depurar). No volver a poner `echo=True` fijo.
- Auth JWT (HS256, secreto hardcodeado en `app/core/config.py`, expira en 24 h). El login es **real**: `POST /api/v1/auth/login` en `app/routers/auth.py` busca en la tabla `usuarios` y verifica con bcrypt (`verify_password`); el token lleva `sub`, `nombre`, `rol` y `empresa_id`. El login hardcodeado que estaba en `main.py` fue eliminado junto con `GET /auth/dev-login`.
- RBAC con dependencias reutilizables en `app/core/security.py`: `get_current_user` (decodifica y da 401) y `require_lectura` / `require_escritura` / `require_admin` (`admin|gestor|conductor` / `admin|gestor` / `admin`). **Todos** los endpoints de órdenes y catálogos exigen token (ya no hay GET anónimos). `empresa_id` **sale del JWT**, no del body: el CRUD filtra por empresa (`_validar_pertenece` rechaza 404 referencias de otra empresa). Ojo: un token antiguo sin `empresa_id` provoca `KeyError` → 500; re-login lo arregla.
- En `app/routers/ordenes.py`, `GET /resumen` está declarado **antes** de `GET /{orden_id}` a propósito: si no, FastAPI lo captura como `orden_id` y da 422.
- Regla de negocio centralizada en `_validar_flota` (`app/crud/crud_ordenes.py`): una flota no supera su capacidad de órdenes activas (`pendiente`/`en_proceso`); se aplica en **crear** y en **editar** (cambio de flota o de estado a activo, excluyendo la propia orden). Un estado `completada` no consume capacidad.
- Catálogos con token: `GET /api/v1/centros`, `/flotas`, `/rutas` (`app/routers/catalogos.py` + `app/crud/crud_catalogos.py`), filtrados por la empresa del JWT. El formulario Angular **sí los consume** (`CatalogoService` + `forkJoin` en `formulario-orden.component.ts`).
- CORS solo permite `localhost:4200`, `127.0.0.1:4200` y hosts sin puerto.
- El frontend llama siempre con **barra final** (`/api/v1/ordenes/`); es intencional.
- CRUD de flotas en `app/routers/catalogos.py` + `app/crud/crud_catalogos.py` (escritura solo `admin`): no se baja la capacidad por debajo de las órdenes activas (400) y no se elimina una flota con órdenes (409).

## Frontend — detalles no obvios

- URL de la API **centralizada** en `src/app/core/config/api.ts` (`API_URL = 'http://127.0.0.1:8000/api/v1'`); todos los servicios pasan por ahí. No hay `environment.ts` ni proxy de dev-server.
- Auth en el frontend: `core/services/auth.service.ts` (`AuthService`) es el único que toca el token (login/logout/`getPayload`/`isLoggedIn`/`hasRole`, clave `token` en `localStorage`). `core/interceptors/auth.interceptor.ts` adjunta el `Bearer` a **todas** las peticiones y hace logout ante cualquier 401 (excepto el propio login) — por eso los servicios ya no mandan headers a mano. Ruta por defecto `''` → `/login`. El **route guard** (`authGuard`) protege las **5** rutas de `app.routes.ts` (`dashboard` + las 4 `/ordenes*`), no así `login`, y valida que el token **no esté vencido** (no solo que exista). Además, `ordenes/nueva` y `ordenes/editar/:id` añaden `roleGuard('admin', 'gestor')` (`core/guards/role.guard.ts`, redirige a `/dashboard` si el rol no calza); la plantilla oculta/muestra botones con `auth.hasRole(...)`.
- **Gotcha de change detection**: `app.config.ts` usa `provideHttpClient(withXhr(), …)` **a propósito**. En Angular 22 el backend por defecto es `fetch` (el de Angular 18+), y `zone.js` 0.16 **no parchea `fetch`** → los callbacks HTTP no corren en NgZone. No quitar `withXhr()` ni "modernizarlo" a fetch sin migrar todo a signals/zoneless. **Pero `withXhr()` solo no basta**: en la carga inicial (F5 directo a la ruta) el repintado por zone tampoco llega tras el HTTP — la respuesta llega **200** en Network y la vista se queda en "Cargando…" para siempre (fallo confirmado en el dashboard). Por eso los 4 componentes que cargan datos en `ngOnInit` (`dashboard`, `detalle-orden`, `formulario-orden`, `listado-ordenes`) llaman `this.cdr.detectChanges()` al final de sus callbacks de suscripción: **es el patrón del repo, conservarlo y usarlo en componentes nuevos** que carguen datos por HTTP.
- **Angular 22 genera archivos SIN sufijo `.component`** (`ng g component foo` → `foo.ts`, clase `Foo`). Este repo usa la convención contraria en código vivo: **renombrar a `foo.component.*` / `FooComponent`** tras generar, o los imports de `app.routes.ts` no coinciden.
- Los stubs de CLI (`app.ts`, `orden.ts` sin `.component`, specs que probaban código muerto) **ya se borraron**: no recrearlos. Hoy los 5 specs (`auth.guard` ×3 con caso de token vencido, `role.guard` ×4, `login`, `dashboard`, `detalle-orden`) prueban solo código real.
- Estilo: Prettier (printWidth 100, single quotes, parser `angular` para HTML) + `.editorconfig` (2 espacios). El repo **no** está formateado hoy (`npx prettier --check .` falla en ~21 archivos): no hacer un formateo masivo, solo formatear los archivos que se toquen.
- Notificaciones con `core/services/toast.service.ts` (signals + `ApplicationRef.tick()` por el gotcha de change detection) y `<app-toast>` en `app.component.html`. Usarlo en vez de `alert()`.
- `core/guards/role.guard.ts`: `roleGuard('admin', 'gestor')` se combina con `authGuard` en `app.routes.ts`. Rutas `/flotas*` son solo admin.
- El detalle de orden resuelve nombres de centro/flota/ruta cargando los catálogos con `forkJoin`.
