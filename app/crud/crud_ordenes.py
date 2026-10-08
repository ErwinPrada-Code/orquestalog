from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from fastapi import HTTPException, status
from app.models.models import Orden, Flota
from app.schemas.schemas import OrdenCreate, OrdenUpdate

async def get_ordenes(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Orden).offset(skip).limit(limit))
    return result.scalars().all()

async def get_orden(db: AsyncSession, orden_id: int):
    result = await db.execute(select(Orden).filter(Orden.id == orden_id))
    return result.scalars().first()

async def create_orden(db: AsyncSession, orden: OrdenCreate):
    # REGLA DE NEGOCIO: Verificar capacidad operativa de la flota
    result_flota = await db.execute(select(Flota).filter(Flota.id == orden.flota_id))
    flota = result_flota.scalars().first()
    
    if not flota:
        raise HTTPException(status_code=404, detail="Flota no encontrada")
        
    # Contar cuántas órdenes activas tiene esta flota
    result_count = await db.execute(
        select(func.count(Orden.id)).filter(Orden.flota_id == orden.flota_id, Orden.estado.in_(['pendiente', 'en_proceso']))
    )
    ordenes_activas = result_count.scalar()
    
    if ordenes_activas >= flota.capacidad:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"La flota {flota.nombre} ha superado su capacidad máxima de {flota.capacidad} órdenes."
        )

    # Crear la orden si pasó la validación
    db_orden = Orden(**orden.model_dump())
    db.add(db_orden)
    await db.commit()
    await db.refresh(db_orden)
    return db_orden

async def update_orden(db: AsyncSession, orden_id: int, orden_data: OrdenUpdate):
    db_orden = await get_orden(db, orden_id)
    if not db_orden:
        return None
        
    for key, value in orden_data.model_dump(exclude_unset=True).items():
        setattr(db_orden, key, value)
        
    await db.commit()
    await db.refresh(db_orden)
    return db_orden

async def delete_orden(db: AsyncSession, orden_id: int):
    db_orden = await get_orden(db, orden_id)
    if db_orden:
        await db.delete(db_orden)
        await db.commit()
    return db_orden