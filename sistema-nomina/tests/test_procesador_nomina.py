"""Pruebas unitarias del procesador de nómina (integración de reglas)."""
from decimal import Decimal

import pytest

from conftest import decimal, hace_anios
from nomina.exceptions import SalarioNetoNegativoError
from nomina.models import PorHoras
from nomina.services import CalculadoraDeducciones, ProcesadorNomina
from nomina.services.deducciones import Deducciones


class DeduccionesExcesivas(CalculadoraDeducciones):
    """Doble de prueba: deducciones mayores al salario bruto.

    Permite verificar la validación de neto negativo, que con las tasas
    reales (5%) es inalcanzable porque el descuento nunca supera el bruto.
    """

    def calcular(self, salario_bruto: Decimal) -> Deducciones:
        return Deducciones(
            seguro_social_pension=salario_bruto * Decimal("0.60"),
            arl=salario_bruto * Decimal("0.60"),
        )


class TestProcesadorNomina:
    def test_nomina_completa_empleado_por_horas(self) -> None:
        """Bruto 950.000 - 5% deducciones = 902.500 neto; sin beneficios."""
        empleado = PorHoras(
            nombre="Bruno",
            identificacion="2",
            fecha_ingreso=hace_anios(2),
            tarifa_por_hora=decimal("20000"),
            horas_trabajadas=decimal("45"),
        )
        recibo = ProcesadorNomina().procesar(empleado)
        assert recibo.salario_bruto == decimal("950000")
        assert recibo.deducciones.total == decimal("47500")
        assert recibo.salario_neto == decimal("902500")
        assert recibo.beneficios.total == 0

    def test_nomina_completa_asalariado_con_antiguedad(self) -> None:
        """Bruto 4.400.000 (con bono 10%); neto = bruto - 5%."""
        from nomina.models import Asalariado

        empleado = Asalariado(
            nombre="Ana",
            identificacion="1",
            fecha_ingreso=hace_anios(6),
            salario_mensual=decimal("4000000"),
        )
        recibo = ProcesadorNomina().procesar(empleado)
        assert recibo.salario_bruto == decimal("4400000")
        assert recibo.deducciones.total == decimal("220000")
        assert recibo.salario_neto == decimal("4180000")
        assert recibo.beneficios.bono_alimentacion == decimal("1000000")

    def test_salario_neto_negativo_lanza_excepcion(self) -> None:
        """El procesador rechaza cualquier recibo con neto negativo."""
        empleado = PorHoras(
            nombre="Bruno",
            identificacion="2",
            fecha_ingreso=hace_anios(2),
            tarifa_por_hora=decimal("20000"),
            horas_trabajadas=decimal("40"),
        )
        procesador = ProcesadorNomina(calculadora_deducciones=DeduccionesExcesivas())
        with pytest.raises(SalarioNetoNegativoError):
            procesador.procesar(empleado)
