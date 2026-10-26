"""Pruebas unitarias de las calculadoras de deducciones y beneficios."""
import pytest

from conftest import decimal, hace_anios
from nomina.models import Asalariado, PorHoras
from nomina.services import CalculadoraBeneficios, CalculadoraDeducciones


class TestCalculadoraDeducciones:
    def test_deducciones_sobre_salario_bruto(self) -> None:
        """SS+Pensión 4% y ARL 1% del salario bruto."""
        deducciones = CalculadoraDeducciones().calcular(decimal("4000000"))
        assert deducciones.seguro_social_pension == decimal("160000")
        assert deducciones.arl == decimal("40000")
        assert deducciones.total == decimal("200000")

    def test_salario_bruto_negativo_es_invalido(self) -> None:
        """No se calculan deducciones sobre un bruto negativo."""
        with pytest.raises(ValueError):
            CalculadoraDeducciones().calcular(decimal("-1"))


class TestCalculadoraBeneficios:
    def _asalariado(self) -> Asalariado:
        return Asalariado(
            nombre="Ana",
            identificacion="1",
            fecha_ingreso=hace_anios(2),
            salario_mensual=decimal("4000000"),
        )

    def _por_horas(self, anios: int, acepta: bool) -> PorHoras:
        return PorHoras(
            nombre="Bruno",
            identificacion="2",
            fecha_ingreso=hace_anios(anios),
            tarifa_por_hora=decimal("20000"),
            horas_trabajadas=decimal("40"),
            acepta_fondo_ahorro=acepta,
        )

    def test_bono_alimentacion_para_permanentes(self) -> None:
        """Los permanentes reciben $1.000.000 de alimentación."""
        beneficios = CalculadoraBeneficios().calcular(self._asalariado(), decimal("4000000"))
        assert beneficios.bono_alimentacion == decimal("1000000")
        assert beneficios.fondo_ahorro == 0
        assert beneficios.total == decimal("1000000")

    def test_fondo_de_ahorro_del_dos_por_ciento(self) -> None:
        """El fondo de ahorro deposita el 2% del salario bruto."""
        empleado = self._por_horas(anios=2, acepta=True)
        beneficios = CalculadoraBeneficios().calcular(empleado, decimal("800000"))
        assert beneficios.fondo_ahorro == decimal("16000")

    def test_sin_beneficios_para_temporal_o_no_elegibles(self) -> None:
        """Sin antigüedad ni aceptación no hay beneficios."""
        empleado = self._por_horas(anios=1, acepta=True)
        beneficios = CalculadoraBeneficios().calcular(empleado, decimal("800000"))
        assert beneficios.total == 0
