from datetime import timedelta

from fastapi.testclient import TestClient
from jose import jwt

from app.core.config import settings
from app.core.security import create_access_token, get_password_hash, verify_password
from app.main import app

client = TestClient(app)

ORDEN = {
    "descripcion": "Lote de prueba",
    "estado": "pendiente",
    "centro_distribucion_id": 1,
    "flota_id": 1,
    "ruta_id": 1,
}
FLOTA = {"nombre": "Camión de prueba", "tipo": "camion", "capacidad": 5}


def _headers(rol: str) -> dict:
    token = create_access_token({"sub": "t@t.com", "nombre": "T", "rol": rol, "empresa_id": 1})
    return {"Authorization": f"Bearer {token}"}


def test_raiz_responde_200():
    assert client.get("/").status_code == 200


def test_hash_y_verificacion_de_password():
    hash_ = get_password_hash("secreto123")
    assert hash_ != "secreto123"
    assert verify_password("secreto123", hash_) is True
    assert verify_password("otra", hash_) is False


def test_verify_password_con_hash_invalido_devuelve_false():
    assert verify_password("x", "esto-no-es-un-hash") is False


def test_token_contiene_rol_y_empresa():
    token = create_access_token({"sub": "t@t.com", "rol": "gestor", "empresa_id": 7})
    datos = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert datos["rol"] == "gestor"
    assert datos["empresa_id"] == 7
    assert "exp" in datos


def test_listar_ordenes_sin_token_devuelve_401():
    assert client.get("/api/v1/ordenes/").status_code == 401


def test_token_invalido_devuelve_401():
    r = client.get("/api/v1/ordenes/", headers={"Authorization": "Bearer basura"})
    assert r.status_code == 401


def test_token_vencido_devuelve_401():
    token = create_access_token(
        {"sub": "t@t.com", "rol": "admin", "empresa_id": 1}, expires_delta=timedelta(minutes=-1)
    )
    r = client.get("/api/v1/ordenes/", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 401


def test_conductor_no_puede_crear_orden():
    r = client.post("/api/v1/ordenes/", json=ORDEN, headers=_headers("conductor"))
    assert r.status_code == 403


def test_gestor_no_puede_eliminar_orden():
    r = client.delete("/api/v1/ordenes/1", headers=_headers("gestor"))
    assert r.status_code == 403


def test_gestor_no_puede_crear_flota():
    r = client.post("/api/v1/flotas", json=FLOTA, headers=_headers("gestor"))
    assert r.status_code == 403
