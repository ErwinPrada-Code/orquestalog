from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

EstadoOrden = Literal["pendiente", "en_proceso", "completada"]
TipoFlota = Literal["camion", "furgoneta", "moto"]


# --- AUTENTICACIÓN ---
class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --- ÓRDENES ---
class OrdenBase(BaseModel):
    descripcion: str = Field(min_length=1, max_length=255)
    estado: EstadoOrden = "pendiente"
    centro_distribucion_id: int
    flota_id: int
    ruta_id: int


class OrdenCreate(OrdenBase):
    pass


class OrdenUpdate(BaseModel):
    descripcion: Optional[str] = Field(default=None, min_length=1, max_length=255)
    estado: Optional[EstadoOrden] = None
    centro_distribucion_id: Optional[int] = None
    flota_id: Optional[int] = None
    ruta_id: Optional[int] = None


class OrdenResponse(OrdenBase):
    id: int
    empresa_id: int
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)


class ResumenOrdenes(BaseModel):
    total: int
    pendientes: int
    en_proceso: int
    completadas: int


# --- CATÁLOGOS ---
class CentroResponse(BaseModel):
    id: int
    nombre: str
    direccion: str
    model_config = ConfigDict(from_attributes=True)


class FlotaResponse(BaseModel):
    id: int
    nombre: str
    tipo: str
    capacidad: int
    model_config = ConfigDict(from_attributes=True)


class FlotaCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    tipo: TipoFlota
    capacidad: int = Field(ge=1, le=1000)


class FlotaUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=100)
    tipo: Optional[TipoFlota] = None
    capacidad: Optional[int] = Field(default=None, ge=1, le=1000)


class RutaResponse(BaseModel):
    id: int
    origen: str
    destino: str
    model_config = ConfigDict(from_attributes=True)
