from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import require_admin, require_lectura
from app.crud import crud_catalogos
from app.schemas.schemas import CentroResponse, FlotaCreate, FlotaResponse, FlotaUpdate, RutaResponse

router = APIRouter(prefix="/api/v1", tags=["Catálogos"])


@router.get("/centros", response_model=List[CentroResponse])
async def read_centros(db: AsyncSession = Depends(get_db), user: dict = Depends(require_lectura)):
    return await crud_catalogos.get_centros(db, user["empresa_id"])


@router.get("/flotas", response_model=List[FlotaResponse])
async def read_flotas(db: AsyncSession = Depends(get_db), user: dict = Depends(require_lectura)):
    return await crud_catalogos.get_flotas(db, user["empresa_id"])


@router.get("/flotas/{flota_id}", response_model=FlotaResponse)
async def read_flota(flota_id: int, db: AsyncSession = Depends(get_db), user: dict = Depends(require_lectura)):
    flota = await crud_catalogos.get_flota(db, flota_id, user["empresa_id"])
    if not flota:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flota no encontrada")
    return flota


@router.post("/flotas", response_model=FlotaResponse, status_code=status.HTTP_201_CREATED)
async def create_flota(flota: FlotaCreate, db: AsyncSession = Depends(get_db), user: dict = Depends(require_admin)):
    return await crud_catalogos.create_flota(db, flota, user["empresa_id"])


@router.put("/flotas/{flota_id}", response_model=FlotaResponse)
async def update_flota(flota_id: int, flota: FlotaUpdate, db: AsyncSession = Depends(get_db), user: dict = Depends(require_admin)):
    db_flota = await crud_catalogos.update_flota(db, flota_id, flota, user["empresa_id"])
    if not db_flota:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flota no encontrada")
    return db_flota


@router.delete("/flotas/{flota_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_flota(flota_id: int, db: AsyncSession = Depends(get_db), user: dict = Depends(require_admin)):
    db_flota = await crud_catalogos.delete_flota(db, flota_id, user["empresa_id"])
    if not db_flota:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flota no encontrada")
    return None


@router.get("/rutas", response_model=List[RutaResponse])
async def read_rutas(db: AsyncSession = Depends(get_db), user: dict = Depends(require_lectura)):
    return await crud_catalogos.get_rutas(db, user["empresa_id"])
