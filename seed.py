import asyncio

from sqlalchemy import select, text

from app.core.database import AsyncSessionLocal, Base, engine
from app.core.security import get_password_hash
from app.models.models import CentroDistribucion, Empresa, Flota, Ruta, Usuario

USUARIOS = [
    ("Administrador", "admin@orquestalog.com", "admin123", "admin"),
    ("Gestor Logístico", "gestor@orquestalog.com", "gestor123", "gestor"),
    ("Conductor", "conductor@orquestalog.com", "conductor123", "conductor"),
]
TABLAS_CON_ID_FIJO = ("empresas", "centros_distribucion", "flotas", "rutas")


async def sembrar(db, modelo, registro_id, **campos):
    if await db.get(modelo, registro_id) is None:
        db.add(modelo(id=registro_id, **campos))


async def init_db():
    print("Creando tablas en la base de datos...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Insertando datos base...")
    async with AsyncSessionLocal() as db:
        await sembrar(db, Empresa, 1, nombre="OrquestaLog Matrix", email="admin@orquestalog.com", telefono="123", direccion="Sede Central")
        await sembrar(db, CentroDistribucion, 1, nombre="Centro Principal Norte", direccion="Norte", empresa_id=1)
        await sembrar(db, CentroDistribucion, 2, nombre="Almacén Regional Sur", direccion="Sur", empresa_id=1)
        await sembrar(db, Flota, 1, nombre="Camión TRK-104", tipo="camion", capacidad=10, empresa_id=1)
        await sembrar(db, Flota, 2, nombre="Furgoneta VAN-332", tipo="furgoneta", capacidad=2, empresa_id=1)
        await sembrar(db, Ruta, 1, origen="Norte", destino="Sur", distancia_km=50.5, tiempo_estimado_minutos=60, empresa_id=1)
        await sembrar(db, Ruta, 2, origen="Centro", destino="Occidente", distancia_km=35.0, tiempo_estimado_minutos=45, empresa_id=1)
        await db.flush()

        for nombre, email, password, rol in USUARIOS:
            existe = (await db.execute(select(Usuario.id).filter(Usuario.email == email))).scalar_one_or_none()
            if existe is None:
                db.add(Usuario(nombre=nombre, email=email, password=get_password_hash(password), rol=rol, empresa_id=1))
        await db.commit()

        # Los ids se insertaron a mano: se alinean las secuencias para futuros INSERT automáticos
        for tabla in TABLAS_CON_ID_FIJO:
            await db.execute(text(f"SELECT setval(pg_get_serial_sequence('{tabla}', 'id'), (SELECT MAX(id) FROM {tabla}))"))
        await db.commit()

    await engine.dispose()
    print("¡Listo! Base de datos inicializada.")


if __name__ == "__main__":
    asyncio.run(init_db())
