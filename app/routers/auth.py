from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.core.security import create_access_token, verify_password
from app.models.models import Usuario
from app.schemas.schemas import LoginRequest, TokenResponse

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticación"])


@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest, db: AsyncSession = Depends(get_db)):
    email = credentials.email.strip().lower()
    result = await db.execute(select(Usuario).filter(Usuario.email == email))
    usuario = result.scalars().first()

    if not usuario or not verify_password(credentials.password, usuario.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario o contraseña incorrectos")

    token = create_access_token(
        data={
            "sub": usuario.email,
            "nombre": usuario.nombre,
            "rol": usuario.rol,
            "empresa_id": usuario.empresa_id,
        }
    )
    return {"access_token": token, "token_type": "bearer"}
