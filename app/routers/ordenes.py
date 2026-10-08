from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.core.security import role_required
from app.schemas.schemas import OrdenResponse, OrdenCreate, OrdenUpdate
from app.crud import crud_ordenes

router = APIRouter(prefix="/api/v1/ordenes", tags=["Órdenes"])

# Lectura permitida para todos los autenticados (incluido 'conductor')
@router.get("/", response_model=List[OrdenResponse])
async def read_ordenes(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud_ordenes.get_ordenes(db, skip=skip, limit=limit)

@router.get("/{orden_id}", response_model=OrdenResponse)
async def read_orden(orden_id: int, db: AsyncSession = Depends(get_db)):
    orden = await crud_ordenes.get_orden(db, orden_id)
    if not orden:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
    return orden

# Creación y actualización solo para admin y gestor logístico
@router.post("/", response_model=OrdenResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(role_required(['admin', 'gestor']))])
async def create_orden(orden: OrdenCreate, db: AsyncSession = Depends(get_db)):
    return await crud_ordenes.create_orden(db, orden)

@router.put("/{orden_id}", response_model=OrdenResponse, dependencies=[Depends(role_required(['admin', 'gestor']))])
async def update_orden(orden_id: int, orden: OrdenUpdate, db: AsyncSession = Depends(get_db)):
    db_orden = await crud_ordenes.update_orden(db, orden_id, orden)
    if not db_orden:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
    return db_orden

# Eliminación EXCLUSIVA para el administrador
@router.delete("/{orden_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(role_required(['admin']))])
async def delete_orden(orden_id: int, db: AsyncSession = Depends(get_db)):
    db_orden = await crud_ordenes.delete_orden(db, orden_id)
    if not db_orden:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
    return None