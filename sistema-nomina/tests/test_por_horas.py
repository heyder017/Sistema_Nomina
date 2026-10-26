"""Pruebas unitarias del empleado por horas."""
import pytest

from conftest import HOY, decimal, hace_anios
from nomina.exceptions import HorasNegativasError
from nomina.models import PorHoras


def crear_por_horas(
    horas: str,
    tarifa: str = "20000",
    anios_antiguedad: int = 0,
    acepta_fondo: bool = False,
) -> PorHoras:
    """Fábrica auxiliar de empleados por horas con parámetros controlados."""
    return PorHoras(
        nombre="Bruno",
        identificacion="456",
        fecha_ingreso=hace_anios(anios_antiguedad),
        tarifa_por_hora=decimal(tarifa),
        horas_trabajadas=decimal(horas),
        acepta_fondo_ahorro=acepta_fondo,
    )


class TestPorHoras:
    def test_pago_horas_normales(self) -> None:
        """Las horas hasta 40 se pagan a tarifa normal."""
        assert crear_por_horas("40").calcular_salario_bruto() == decimal("800000")

    def test_pago_horas_extras_a_1_5(self) -> None:
        """Las horas mayores a 40 se pagan 1.5 x tarifa."""
        empleado = crear_por_horas("45")
        assert empleado.horas_extras() == decimal("5")
        assert empleado.monto_horas_extras() == decimal("150000")
        assert empleado.calcular_salario_bruto() == decimal("950000")

    def test_horas_negativas_son_invalidas(self) -> None:
        """Las horas trabajadas no pueden ser negativas."""
        with pytest.raises(HorasNegativasError):
            crear_por_horas("-1")

    def test_no_recibe_bonos_de_alimentacion(self) -> None:
        """El empleado por horas no es permanente: sin bono de alimentación."""
        empleado = crear_por_horas("40", anios_antiguedad=6)
        assert empleado.es_permanente is False
        assert empleado.calcular_salario_bruto() == decimal("800000")

    def test_accede_al_fondo_con_mas_de_un_anio_y_aceptacion(self) -> None:
        """Con > 1 año y aceptando el fondo, accede a él."""
        assert crear_por_horas("40", 1, anios_antiguedad=2, acepta_fondo=True).accede_fondo_ahorro(HOY)

    def test_no_accede_al_fondo_si_no_acepta(self) -> None:
        """Aunque tenga antigüedad, sin aceptar no accede al fondo."""
        assert crear_por_horas("40", 1, anios_antiguedad=2, acepta_fondo=False).accede_fondo_ahorro(HOY) is False

    def test_no_accede_al_fondo_con_un_anio_o_menos(self) -> None:
        """Se exige superar 1 año de antigüedad para el fondo."""
        assert crear_por_horas("40", 1, anios_antiguedad=1, acepta_fondo=True).accede_fondo_ahorro(HOY) is False
