"""Servicio de deducciones obligatorias.

Responsabilidad única (SRP): calcular únicamente las deducciones de ley
sobre el salario bruto. No conoce beneficios ni tipos concretos de empleado.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from nomina.config import PARAMETROS_POR_DEFECTO, ParametrosNomina


@dataclass(frozen=True)
class Deducciones:
    """Detalle de las deducciones obligatorias de un periodo."""

    seguro_social_pension: Decimal
    arl: Decimal

    @property
    def total(self) -> Decimal:
        """Suma de todas las deducciones obligatorias."""
        return self.seguro_social_pension + self.arl


class CalculadoraDeducciones:
    """Calcula las deducciones obligatorias a partir del salario bruto."""

    def __init__(self, parametros: ParametrosNomina = PARAMETROS_POR_DEFECTO) -> None:
        self._parametros = parametros

    def calcular(self, salario_bruto: Decimal) -> Deducciones:
        """Aplica SS+Pensión (4%) y ARL (1%) sobre el salario bruto."""
        if salario_bruto < 0:
            raise ValueError("El salario bruto no puede ser negativo.")
        return Deducciones(
            seguro_social_pension=salario_bruto * self._parametros.tasa_seguro_social_pension,
            arl=salario_bruto * self._parametros.tasa_arl,
        )
