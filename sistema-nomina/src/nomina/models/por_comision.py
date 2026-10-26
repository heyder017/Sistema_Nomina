"""Empleado por comisión: salario base + porcentaje sobre ventas."""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from nomina.config import PARAMETROS_POR_DEFECTO, ParametrosNomina
from nomina.exceptions import VentasNegativasError
from nomina.models.empleado import Empleado


@dataclass(frozen=True)
class PorComision(Empleado):
    """Empleado con salario base más comisión sobre ventas.

    Reglas de negocio:
        * Salario base + porcentaje de comisión sobre ventas.
        * Si las ventas superan $20.000.000, recibe un bono adicional
          del 3% sobre las ventas.
    """

    salario_base: Decimal = Decimal("0")
    porcentaje_comision: Decimal = Decimal("0")
    ventas: Decimal = Decimal("0")
    parametros: ParametrosNomina = PARAMETROS_POR_DEFECTO

    def __post_init__(self) -> None:
        super().__post_init__()
        # Validación: las ventas no pueden ser menores a $0.
        if self.ventas < 0:
            raise VentasNegativasError(
                f"Las ventas no pueden ser negativas: {self.ventas}."
            )
        if self.salario_base < 0:
            raise ValueError(f"El salario base no puede ser negativo: {self.salario_base}.")

    @property
    def es_permanente(self) -> bool:
        """Los empleados por comisión son permanentes."""
        return True

    def monto_comision(self) -> Decimal:
        """Valor de la comisión sobre las ventas del periodo."""
        return self.ventas * self.porcentaje_comision

    def bono_por_ventas_altas(self) -> Decimal:
        """Bono del 3% sobre las ventas cuando superan el umbral definido."""
        if self.ventas > self.parametros.umbral_ventas_bono_comision:
            return self.ventas * self.parametros.tasa_bono_comision
        return Decimal("0")

    def calcular_salario_bruto(self) -> Decimal:
        """Salario base + comisión + bono por ventas altas (si aplica)."""
        return self.salario_base + self.monto_comision() + self.bono_por_ventas_altas()
