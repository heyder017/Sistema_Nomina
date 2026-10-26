"""Empleado temporal: salario fijo en contrato por tiempo definido."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from nomina.models.empleado import Empleado


@dataclass(frozen=True)
class Temporal(Empleado):
    """Empleado con contrato a término fijo.

    Reglas de negocio:
        * Salario fijo mensual.
        * Contrato por tiempo definido (fecha de fin de contrato).
        * No aplican bonos ni beneficios adicionales.
    """

    salario_mensual: Decimal = Decimal("0")
    fecha_fin_contrato: date | None = None

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.salario_mensual < 0:
            raise ValueError(
                f"El salario mensual no puede ser negativo: {self.salario_mensual}."
            )
        if self.fecha_fin_contrato is not None and self.fecha_fin_contrato <= self.fecha_ingreso:
            raise ValueError(
                "La fecha de fin de contrato debe ser posterior a la fecha de ingreso."
            )

    def contrato_vigente(self, fecha_referencia: date | None = None) -> bool:
        """Indica si la fecha de referencia cae dentro del contrato."""
        if self.fecha_fin_contrato is None:
            return True
        referencia = fecha_referencia or date.today()
        return self.fecha_ingreso <= referencia <= self.fecha_fin_contrato

    def calcular_salario_bruto(self) -> Decimal:
        """Salario fijo mensual del contrato; sin bonos ni beneficios."""
        return self.salario_mensual
