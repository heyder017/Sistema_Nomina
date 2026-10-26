"""Servicio de beneficios adicionales.

Responsabilidad única (SRP): decidir y calcular los beneficios que aplica a
cada empleado. Consulta el modelo a través de su contrato (``es_permanente``,
``accede_fondo_ahorro``) sin usar ``isinstance``, de modo que el alta de un
nuevo tipo de empleado no requiere modificar esta clase (OCP).
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from nomina.config import PARAMETROS_POR_DEFECTO, ParametrosNomina
from nomina.models.empleado import Empleado


@dataclass(frozen=True)
class Beneficios:
    """Detalle de los beneficios adicionales de un periodo."""

    bono_alimentacion: Decimal
    fondo_ahorro: Decimal

    @property
    def total(self) -> Decimal:
        """Suma de todos los beneficios del periodo."""
        return self.bono_alimentacion + self.fondo_ahorro


class CalculadoraBeneficios:
    """Calcula los beneficios adicionales según el tipo de empleado."""

    def __init__(self, parametros: ParametrosNomina = PARAMETROS_POR_DEFECTO) -> None:
        self._parametros = parametros

    def calcular_bono_alimentacion(self, empleado: Empleado) -> Decimal:
        """Bono de alimentación de $1.000.000 solo para permanentes."""
        if empleado.es_permanente:
            return self._parametros.bono_alimentacion
        return Decimal("0")

    def calcular_fondo_ahorro(
        self, empleado: Empleado, salario_bruto: Decimal
    ) -> Decimal:
        """2% del salario depositado si el empleado accede al fondo."""
        if empleado.accede_fondo_ahorro():
            return salario_bruto * self._parametros.tasa_fondo_ahorro
        return Decimal("0")

    def calcular(
        self, empleado: Empleado, salario_bruto: Decimal
    ) -> Beneficios:
        """Calcula todos los beneficios aplicables al empleado."""
        return Beneficios(
            bono_alimentacion=self.calcular_bono_alimentacion(empleado),
            fondo_ahorro=self.calcular_fondo_ahorro(empleado, salario_bruto),
        )
