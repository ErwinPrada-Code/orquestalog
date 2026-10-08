from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.models import CentroDistribucion, Flota, Orden, Ruta
from app.schemas.schemas import OrdenCreate, OrdenUpdate

ESTADOS_ACTIVOS = ("pendiente", "en_proceso")


async def _validar_pertenece(db: AsyncSession, modelo, registro_id: int, empresa_id: int, nombre: str):
    result = await db.execute(
        select(modelo.id).filter(modelo.id == registro_id, modelo.empresa_id == empresa_id)
    )
    if result.scalar_one_or_none() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{nombre} no encontrado")


async def _validar_flota(
    db: AsyncSession,
    flota_id: int,
    empresa_id: int,
    validar_capacidad: bool,
    excluir_orden_id: int | None = None,
):
    """REGLA DE NEGOCIO: una flota no puede superar su capacidad de órdenes activas."""
    result = await db.execute(
        select(Flota).filter(Flota.id == flota_id, Flota.empresa_id == empresa_id)
    )
    flota = result.scalars().first()
    if not flota:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flota no encontrada")
    if not validar_capacidad:
        return

    consulta = select(func.count(Orden.id)).filter(
        Orden.flota_id == flota_id, Orden.estado.in_(ESTADOS_ACTIVOS)
    )
    if excluir_orden_id is not None:
        consulta = consulta.filter(Orden.id != excluir_orden_id)
    activas = (await db.execute(consulta)).scalar_one()

    if activas >= flota.capacidad:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La flota {flota.nombre} ha superado su capacidad máxima de {flota.capacidad} órdenes activas.",
        )


async def get_ordenes(db: AsyncSession, empresa_id: int, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Orden)
        .filter(Orden.empresa_id == empresa_id)
        .order_by(Orden.id.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_orden(db: AsyncSession, orden_id: int, empresa_id: int):
    result = await db.execute(
        select(Orden).filter(Orden.id == orden_id, Orden.empresa_id == empresa_id)
    )
    return result.scalars().first()


async def get_resumen(db: AsyncSession, empresa_id: int) -> dict:
    result = await db.execute(
        select(Orden.estado, func.count(Orden.id))
        .filter(Orden.empresa_id == empresa_id)
        .group_by(Orden.estado)
    )
    conteo = {estado: total for estado, total in result.all()}
    return {
        "total": sum(conteo.values()),
        "pendientes": conteo.get("pendiente", 0),
        "en_proceso": conteo.get("en_proceso", 0),
        "completadas": conteo.get("completada", 0),
    }


async def create_orden(db: AsyncSession, orden: OrdenCreate, empresa_id: int):
    await _validar_pertenece(db, CentroDistribucion, orden.centro_distribucion_id, empresa_id, "Centro de distribución")
    await _validar_pertenece(db, Ruta, orden.ruta_id, empresa_id, "Ruta")
    await _validar_flota(db, orden.flota_id, empresa_id, validar_capacidad=orden.estado in ESTADOS_ACTIVOS)

    db_orden = Orden(**orden.model_dump(), empresa_id=empresa_id)
    db.add(db_orden)
    await db.commit()
    await db.refresh(db_orden)
    return db_orden


async def update_orden(db: AsyncSession, orden_id: int, orden_data: OrdenUpdate, empresa_id: int):
    db_orden = await get_orden(db, orden_id, empresa_id)
    if not db_orden:
        return None

    cambios = orden_data.model_dump(exclude_unset=True, exclude_none=True)
    nuevo_estado = cambios.get("estado", db_orden.estado)
    nueva_flota = cambios.get("flota_id", db_orden.flota_id)

    if "centro_distribucion_id" in cambios:
        await _validar_pertenece(db, CentroDistribucion, cambios["centro_distribucion_id"], empresa_id, "Centro de distribución")
    if "ruta_id" in cambios:
        await _validar_pertenece(db, Ruta, cambios["ruta_id"], empresa_id, "Ruta")

    flota_cambio = nueva_flota != db_orden.flota_id
    estaba_activa = db_orden.estado in ESTADOS_ACTIVOS
    if nuevo_estado in ESTADOS_ACTIVOS and (flota_cambio or not estaba_activa):
        await _validar_flota(db, nueva_flota, empresa_id, validar_capacidad=True, excluir_orden_id=orden_id)
    elif flota_cambio:
        await _validar_flota(db, nueva_flota, empresa_id, validar_capacidad=False)

    for key, value in cambios.items():
        setattr(db_orden, key, value)

    await db.commit()
    await db.refresh(db_orden)
    return db_orden


async def delete_orden(db: AsyncSession, orden_id: int, empresa_id: int):
    db_orden = await get_orden(db, orden_id, empresa_id)
    if db_orden:
        await db.delete(db_orden)
        await db.commit()
    return db_orden
