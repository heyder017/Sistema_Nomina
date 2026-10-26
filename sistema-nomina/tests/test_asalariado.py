"""Pruebas unitarias del empleado asalariado."""
from decimal import Decimal

import pytest

from conftest import HOY, decimal, hace_anios
from nomina.models import Asalariado


def crear_asalariado(salario: str, anios_antiguedad: int) -> Asalariado:
    """Fábrica auxiliar de asalariados con antigüedad controlada."""
    return Asalariado(
        nombre="Ana",
        identificacion="123",
        fecha_ingreso=hace_anios(anios_antiguedad),
        salario_mensual=decimal(salario),
    )


class TestAsalariado:
    def test_salario_bruto_sin_antiguedad_suficiente(self) -> None:
        """Sin más de 5 años el bruto es solo el salario mensual."""
        empleado = crear_asalariado("4000000", anios_antiguedad=3)
        assert empleado.calcular_salario_bruto() == decimal("4000000")
        assert empleado.bono_antiguedad(HOY) == 0

    def test_bono_antiguedad_del_10_por_ciento(self) -> None:
        """Con más de 5 años aplica el bono del 10%."""
        empleado = crear_asalariado("4000000", anios_antiguedad=6)
        assert empleado.bono_antiguedad(HOY) == decimal("400000")
        assert empleado.calcular_salario_bruto() == decimal("4400000")

    def test_bono_no_aplica_exactamente_5_anios(self) -> None:
        """El bono exige superar los 5 años (estrictamente mayor)."""
        empleado = crear_asalariado("4000000", anios_antiguedad=5)
        assert empleado.bono_antiguedad(HOY) == 0

    def test_es_empleado_permanente(self) -> None:
        """El asalariado se considera permanente para beneficios."""
        assert crear_asalariado("1000000", 1).es_permanente is True

    def test_nombre_vacio_es_invalido(self) -> None:
        """El nombre no puede estar vacío (invariante del dominio)."""
        with pytest.raises(ValueError):
            Asalariado(
                nombre="  ",
                identificacion="123",
                fecha_ingreso=HOY,
                salario_mensual=Decimal("0"),
            )
