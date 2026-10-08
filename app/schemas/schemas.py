from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# --- ESQUEMAS PARA ÓRDENES ---
class OrdenBase(BaseModel):
    descripcion: str
    estado: str = "pendiente"
    centro_distribucion_id: int
    flota_id: int
    ruta_id: int
    empresa_id: int

class OrdenCreate(OrdenBase):
    pass

class OrdenUpdate(BaseModel):
    descripcion: Optional[str] = None
    estado: Optional[str] = None
    centro_distribucion_id: Optional[int] = None
    flota_id: Optional[int] = None
    ruta_id: Optional[int] = None

class OrdenResponse(OrdenBase):
    id: int
    fecha_creacion: datetime
    
    # Esto permite traducir de SQLAlchemy a JSON automáticamente
    model_config = ConfigDict(from_attributes=True)