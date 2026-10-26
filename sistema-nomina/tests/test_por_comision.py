"""Pruebas unitarias del empleado por comisión."""
import pytest

from conftest import HOY, decimal, hace_anios
from nomina.exceptions import VentasNegativasError
from nomina.models import PorComision


def crear_por_comision(
    ventas: str,
    salario_base: str = "1500000",
    comision: str = "0.05",
) -> PorComision:
    """Fábrica auxiliar de empleados por comisión."""
    return PorComision(
        nombre="Carla",
        identificacion="789",
        fecha_ingreso=hace_anios(3),
        salario_base=decimal(salario_base),
        porcentaje_comision=decimal(comision),
        ventas=decimal(ventas),
    )


class TestPorComision:
    def test_salario_base_mas_comision(self) -> None:
        """El bruto es salario base + comisión sobre ventas."""
        assert crear_por_comision("10000000").calcular_salario_bruto() == decimal("2000000")

    def test_bono_por_ventas_sobre_20_millones(self) -> None:
        """Ventas > $20.000.000 generan bono del 3% sobre las ventas."""
        empleado = crear_por_comision("25000000")
        assert empleado.bono_por_ventas_altas() == decimal("750000")
        # 1.500.000 + 5% de 25M (1.250.000) + 3% de 25M (750.000)
        assert empleado.calcular_salario_bruto() == decimal("3500000")

    def test_sin_bono_con_ventas_en_el_umbral(self) -> None:
        """Exactamente $20.000.000 no supera el umbral: sin bono."""
        assert crear_por_comision("20000000").bono_por_ventas_altas() == 0

    def test_ventas_negativas_son_invalidas(self) -> None:
        """Las ventas no pueden ser menores a $0."""
        with pytest.raises(VentasNegativasError):
            crear_por_comision("-1000")

    def test_es_empleado_permanente(self) -> None:
        """El empleado por comisión es permanente para beneficios."""
        assert crear_por_comision("0").es_permanente is True
