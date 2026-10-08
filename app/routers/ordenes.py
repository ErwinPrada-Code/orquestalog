from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import require_admin, require_escritura, require_lectura
from app.crud import crud_ordenes
from app.schemas.schemas import OrdenCreate, OrdenResponse, OrdenUpdate, ResumenOrdenes

router = APIRouter(prefix="/api/v1/ordenes", tags=["Órdenes"])


@router.get("/", response_model=List[OrdenResponse])
async def read_ordenes(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(require_lectura),
):
    return await crud_ordenes.get_ordenes(db, user["empresa_id"], skip=skip, limit=limit)


@router.get("/resumen", response_model=ResumenOrdenes)
async def read_resumen(db: AsyncSession = Depends(get_db), user: dict = Depends(require_lectura)):
    return await crud_ordenes.get_resumen(db, user["empresa_id"])


@router.get("/{orden_id}", response_model=OrdenResponse)
async def read_orden(orden_id: int, db: AsyncSession = Depends(get_db), user: dict = Depends(require_lectura)):
    orden = await crud_ordenes.get_orden(db, orden_id, user["empresa_id"])
    if not orden:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
    return orden


@router.post("/", response_model=OrdenResponse, status_code=status.HTTP_201_CREATED)
async def create_orden(orden: OrdenCreate, db: AsyncSession = Depends(get_db), user: dict = Depends(require_escritura)):
    return await crud_ordenes.create_orden(db, orden, user["empresa_id"])


@router.put("/{orden_id}", response_model=OrdenResponse)
async def update_orden(orden_id: int, orden: OrdenUpdate, db: AsyncSession = Depends(get_db), user: dict = Depends(require_escritura)):
    db_orden = await crud_ordenes.update_orden(db, orden_id, orden, user["empresa_id"])
    if not db_orden:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
    return db_orden


@router.delete("/{orden_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_orden(orden_id: int, db: AsyncSession = Depends(get_db), user: dict = Depends(require_admin)):
    db_orden = await crud_ordenes.delete_orden(db, orden_id, user["empresa_id"])
    if not db_orden:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
    return None
