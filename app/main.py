from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.routers import ordenes
from app.core.security import create_access_token # <-- Nueva importación


app = FastAPI(
    title="API de OrquestaLog",
    description="Sistema de Orquestación Logística Multiempresa",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200", "http://localhost", "http://127.0.0.1"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ordenes.router)

@app.get("/")
def root():
    return {"mensaje": "La API de OrquestaLog está en línea y funcionando"}

# Esquema para recibir los datos del formulario
class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/api/v1/auth/login")
def login(credentials: LoginRequest):
    # Credenciales de administrador por defecto para la sustentación
    if credentials.email == "admin@orquestalog.com" and credentials.password == "admin123":
        token = create_access_token(data={"sub": credentials.email, "rol": "admin"})
        return {"access_token": token}

    raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")