from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.crud_ordenes import ESTADOS_ACTIVOS
from app.models.models import CentroDistribucion, Flota, Orden, Ruta
from app.schemas.schemas import FlotaCreate, FlotaUpdate


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


# --- CRUD DE FLOTAS ---
async def get_flota(db: AsyncSession, flota_id: int, empresa_id: int):
    result = await db.execute(
        select(Flota).filter(Flota.id == flota_id, Flota.empresa_id == empresa_id)
    )
    return result.scalars().first()


async def _contar_ordenes(db: AsyncSession, flota_id: int, solo_activas: bool) -> int:
    consulta = select(func.count(Orden.id)).filter(Orden.flota_id == flota_id)
    if solo_activas:
        consulta = consulta.filter(Orden.estado.in_(ESTADOS_ACTIVOS))
    return (await db.execute(consulta)).scalar_one()


async def create_flota(db: AsyncSession, flota: FlotaCreate, empresa_id: int):
    db_flota = Flota(**flota.model_dump(), empresa_id=empresa_id)
    db.add(db_flota)
    await db.commit()
    await db.refresh(db_flota)
    return db_flota


async def update_flota(db: AsyncSession, flota_id: int, datos: FlotaUpdate, empresa_id: int):
    db_flota = await get_flota(db, flota_id, empresa_id)
    if not db_flota:
        return None

    cambios = datos.model_dump(exclude_unset=True, exclude_none=True)

    if "capacidad" in cambios:
        activas = await _contar_ordenes(db, flota_id, solo_activas=True)
        if cambios["capacidad"] < activas:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se puede reducir la capacidad a {cambios['capacidad']}: la flota tiene {activas} órdenes activas.",
            )

    for key, value in cambios.items():
        setattr(db_flota, key, value)

    await db.commit()
    await db.refresh(db_flota)
    return db_flota


async def delete_flota(db: AsyncSession, flota_id: int, empresa_id: int):
    db_flota = await get_flota(db, flota_id, empresa_id)
    if not db_flota:
        return None

    total = await _contar_ordenes(db, flota_id, solo_activas=False)
    if total > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"No se puede eliminar la flota: tiene {total} órdenes asociadas.",
        )

    await db.delete(db_flota)
    await db.commit()
    return db_flota
