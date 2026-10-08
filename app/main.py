from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, catalogos, ordenes

app = FastAPI(
    title="API de OrquestaLog",
    description="Sistema de Orquestación Logística Multiempresa",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200", "http://localhost", "http://127.0.0.1"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(catalogos.router)
app.include_router(ordenes.router)


@app.get("/")
def root():
    return {"mensaje": "La API de OrquestaLog está en línea y funcionando"}
