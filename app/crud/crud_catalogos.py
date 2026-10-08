from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.models import CentroDistribucion, Flota, Ruta


async def _listar(db: AsyncSession, modelo, empresa_id: int):
    result = await db.execute(
        select(modelo).filter(modelo.empresa_id == empresa_id).order_by(modelo.id)
    )
    return result.scalars().all()


async def get_centros(db: AsyncSession, empresa_id: int):
    return await _listar(db, CentroDistribucion, empresa_id)


async def get_flotas(db: AsyncSession, empresa_id: int):
    return await _listar(db, Flota, empresa_id)


async def get_rutas(db: AsyncSession, empresa_id: int):
    return await _listar(db, Ruta, empresa_id)
