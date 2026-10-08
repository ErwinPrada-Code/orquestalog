import asyncio
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.crud import crud_catalogos, crud_ordenes
from app.schemas.schemas import FlotaUpdate


class FakeResult:
    def __init__(self, valor):
        self.valor = valor

    def scalars(self):
        return self

    def first(self):
        return self.valor

    def scalar_one(self):
        return self.valor


class FakeDB:
    """Devuelve los resultados en el orden en que el CRUD ejecuta sus consultas."""

    def __init__(self, *resultados):
        self.resultados = list(resultados)

    async def execute(self, _consulta):
        return self.resultados.pop(0)


FLOTA = SimpleNamespace(id=1, nombre="TRK-104", capacidad=2)


def test_flota_inexistente_devuelve_404():
    db = FakeDB(FakeResult(None))
    with pytest.raises(HTTPException) as exc:
        asyncio.run(crud_ordenes._validar_flota(db, 99, 1, validar_capacidad=True))
    assert exc.value.status_code == 404


def test_flota_llena_rechaza_la_orden_con_400():
    db = FakeDB(FakeResult(FLOTA), FakeResult(2))
    with pytest.raises(HTTPException) as exc:
        asyncio.run(crud_ordenes._validar_flota(db, 1, 1, validar_capacidad=True))
    assert exc.value.status_code == 400
    assert "capacidad máxima" in exc.value.detail


def test_flota_con_cupo_acepta_la_orden():
    db = FakeDB(FakeResult(FLOTA), FakeResult(1))
    asyncio.run(crud_ordenes._validar_flota(db, 1, 1, validar_capacidad=True))


def test_orden_completada_no_consume_capacidad():
    db = FakeDB(FakeResult(FLOTA))  # solo se ejecuta la consulta de la flota
    asyncio.run(crud_ordenes._validar_flota(db, 1, 1, validar_capacidad=False))
    assert db.resultados == []


def test_no_se_puede_bajar_capacidad_por_debajo_de_ordenes_activas():
    db = FakeDB(FakeResult(FLOTA), FakeResult(2))
    with pytest.raises(HTTPException) as exc:
        asyncio.run(crud_catalogos.update_flota(db, 1, FlotaUpdate(capacidad=1), 1))
    assert exc.value.status_code == 400


def test_no_se_puede_eliminar_flota_con_ordenes():
    db = FakeDB(FakeResult(FLOTA), FakeResult(3))
    with pytest.raises(HTTPException) as exc:
        asyncio.run(crud_catalogos.delete_flota(db, 1, 1))
    assert exc.value.status_code == 409
