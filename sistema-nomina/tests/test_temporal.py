"""Pruebas unitarias del empleado temporal."""
from datetime import date
from decimal import Decimal

import pytest

from conftest import HOY, decimal, hace_anios
from nomina.models import Temporal


def crear_temporal(
    salario: str = "2000000",
    fecha_ingreso: date | None = None,
    fecha_fin: date | None = None,
) -> Temporal:
    """Fábrica auxiliar de empleados temporales."""
    ingreso = fecha_ingreso or date(HOY.year, 1, 1)
    return Temporal(
        nombre="Diego",
        identificacion="101112",
        fecha_ingreso=ingreso,
        salario_mensual=decimal(salario),
        fecha_fin_contrato=fecha_fin or date(HOY.year, 12, 31),
    )


class TestTemporal:
    def test_salario_bruto_es_salario_fijo(self) -> None:
        """El temporal cobra únicamente su salario fijo mensual."""
        assert crear_temporal("2000000").calcular_salario_bruto() == decimal("2000000")

    def test_no_es_permanente(self) -> None:
        """El temporal no recibe beneficios de empleados permanentes."""
        assert crear_temporal().es_permanente is False

    def test_contrato_vigente(self) -> None:
        """Dentro del rango del contrato el empleado está vigente."""
        assert crear_temporal().contrato_vigente(HOY) is True

    def test_contrato_vencido(self) -> None:
        """Después de la fecha fin el contrato ya no está vigente."""
        empleado = crear_temporal(fecha_fin=date(HOY.year, 6, 30))
        assert empleado.contrato_vigente(HOY) is False

    def test_fin_de_contrato_debe_ser_posterior_al_ingreso(self) -> None:
        """La fecha fin debe ser posterior a la fecha de ingreso."""
        with pytest.raises(ValueError):
            crear_temporal(
                fecha_ingreso=date(2026, 1, 1),
                fecha_fin=date(2025, 12, 31),
            )

    def test_salario_negativo_es_invalido(self) -> None:
        """El salario mensual no puede ser negativo."""
        with pytest.raises(ValueError):
            crear_temporal(salario="-1")
