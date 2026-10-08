from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import require_lectura
from app.crud import crud_catalogos
from app.schemas.schemas import CentroResponse, FlotaResponse, RutaResponse

router = APIRouter(prefix="/api/v1", tags=["Catálogos"])


@router.get("/centros", response_model=List[CentroResponse])
async def read_centros(db: AsyncSession = Depends(get_db), user: dict = Depends(require_lectura)):
    return await crud_catalogos.get_centros(db, user["empresa_id"])


@router.get("/flotas", response_model=List[FlotaResponse])
async def read_flotas(db: AsyncSession = Depends(get_db), user: dict = Depends(require_lectura)):
    return await crud_catalogos.get_flotas(db, user["empresa_id"])


@router.get("/rutas", response_model=List[RutaResponse])
async def read_rutas(db: AsyncSession = Depends(get_db), user: dict = Depends(require_lectura)):
    return await crud_catalogos.get_rutas(db, user["empresa_id"])
