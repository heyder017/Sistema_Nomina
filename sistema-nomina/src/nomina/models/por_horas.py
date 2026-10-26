"""Empleado por horas: pago por horas trabajadas + extras a 1.5x."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from nomina.config import PARAMETROS_POR_DEFECTO, ParametrosNomina
from nomina.exceptions import HorasNegativasError
from nomina.models.empleado import Empleado


@dataclass(frozen=True)
class PorHoras(Empleado):
    """Empleado remunerado por horas trabajadas en el periodo.

    Reglas de negocio:
        * Pago por horas trabajadas a tarifa base por hora.
        * Horas extras (más de 40) se pagan a 1.5 x la tarifa normal.
        * No recibe bonos.
        * Con más de 1 año en la empresa puede acceder al fondo de ahorro
          (2% del salario depositado mensualmente) si acepta el acceso.
    """

    tarifa_por_hora: Decimal = Decimal("0")
    horas_trabajadas: Decimal = Decimal("0")
    acepta_fondo_ahorro: bool = False
    parametros: ParametrosNomina = PARAMETROS_POR_DEFECTO

    def __post_init__(self) -> None:
        super().__post_init__()
        # Validación: las horas trabajadas no pueden ser negativas.
        if self.horas_trabajadas < 0:
            raise HorasNegativasError(
                f"Las horas trabajadas no pueden ser negativas: {self.horas_trabajadas}."
            )
        if self.tarifa_por_hora < 0:
            raise ValueError(f"La tarifa por hora no puede ser negativa: {self.tarifa_por_hora}.")

    def horas_extras(self) -> Decimal:
        """Cantidad de horas que superan las horas regulares del periodo."""
        return max(Decimal("0"), self.horas_trabajadas - self.parametros.horas_regulares)

    def monto_horas_extras(self) -> Decimal:
        """Valor pagado por las horas extras a 1.5 x la tarifa normal."""
        return (
            self.horas_extras()
            * self.parametros.multiplicador_horas_extras
            * self.tarifa_por_hora
        )

    def accede_fondo_ahorro(self, fecha_referencia: date | None = None) -> bool:
        """True si tiene > 1 año de antigüedad y aceptó el fondo de ahorro."""
        return self.acepta_fondo_ahorro and self.tiene_mas_anios_que(
            self.parametros.anios_minimos_fondo_ahorro, fecha_referencia
        )

    def calcular_salario_bruto(self) -> Decimal:
        """Horas normales a tarifa base + horas extras a 1.5 x tarifa."""
        horas_normales = min(self.horas_trabajadas, self.parametros.horas_regulares)
        return horas_normales * self.tarifa_por_hora + self.monto_horas_extras()
