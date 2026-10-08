import asyncio
from app.core.database import engine, Base, AsyncSessionLocal
from app.models.models import Empresa, CentroDistribucion, Flota, Ruta

async def init_db():
    print("Creando tablas en la base de datos...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("Insertando datos por defecto para el frontend...")
    async with AsyncSessionLocal() as db:
        # Creamos los datos que el formulario de Angular necesita por defecto
        empresa = Empresa(id=1, nombre="OrquestaLog Matrix", email="admin@orquestalog.com", telefono="123", direccion="Sede Central")
        centro = CentroDistribucion(id=1, nombre="Centro Principal Norte", direccion="Norte", empresa_id=1)
        flota = Flota(id=1, nombre="Camión TRK-104", tipo="camion", capacidad=10, empresa_id=1)
        ruta = Ruta(id=1, origen="Norte", destino="Sur", distancia_km=50.5, tiempo_estimado_minutos=60, empresa_id=1)
        
        db.add_all([empresa, centro, flota, ruta])
        try:
            await db.commit()
            print("¡Éxito! Base de datos inicializada. Ya puedes crear órdenes.")
        except Exception as e:
            print("Nota: Los datos ya existían o hubo un aviso:", e)

asyncio.run(init_db())