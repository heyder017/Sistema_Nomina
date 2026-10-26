"""Empleado asalariado: salario fijo mensual + bono de antigüedad."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from nomina.config import PARAMETROS_POR_DEFECTO, ParametrosNomina
from nomina.models.empleado import Empleado


@dataclass(frozen=True)
class Asalariado(Empleado):
    """Empleado con salario fijo mensual.

    Regla de negocio:
        * Bono mensual del 10% del salario si lleva más de 5 años en la empresa.
    """

    salario_mensual: Decimal = Decimal("0")
    parametros: ParametrosNomina = PARAMETROS_POR_DEFECTO

    @property
    def es_permanente(self) -> bool:
        """Los asalariados son empleados permanentes."""
        return True

    def bono_antiguedad(self, fecha_referencia: date | None = None) -> Decimal:
        """Bono del 10% del salario si la antigüedad supera los 5 años."""
        if self.tiene_mas_anios_que(
            self.parametros.anios_minimos_bono_antiguedad, fecha_referencia
        ):
            return self.salario_mensual * self.parametros.tasa_bono_antiguedad
        return Decimal("0")

    def calcular_salario_bruto(self) -> Decimal:
        """Salario fijo mensual más el bono de antigüedad cuando aplique."""
        return self.salario_mensual + self.bono_antiguedad()
