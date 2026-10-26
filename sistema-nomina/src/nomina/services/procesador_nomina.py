"""Procesador de nómina: orquesta el cálculo completo de un empleado.

Coordina a los servicios de deducciones y beneficios sin implementar sus
reglas (SRP). Depende de abstracciones (Empleado y las calculadoras), no de
concreciones concretas acopladas, lo que permite sustituir cualquiera de
ellas (DIP) y añadir nuevos tipos de empleado sin tocar esta clase (OCP).
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from nomina.exceptions import SalarioNetoNegativoError
from nomina.models.empleado import Empleado
from nomina.services.beneficios import Beneficios, CalculadoraBeneficios
from nomina.services.deducciones import CalculadoraDeducciones, Deducciones


@dataclass(frozen=True)
class ReciboNomina:
    """Resultado del cálculo de nómina de un empleado en un periodo."""

    empleado: Empleado
    salario_bruto: Decimal
    deducciones: Deducciones
    beneficios: Beneficios

    @property
    def salario_neto(self) -> Decimal:
        """Salario bruto menos deducciones obligatorias."""
        return self.salario_bruto - self.deducciones.total


class ProcesadorNomina:
    """Calcula la nómina completa de cualquier empleado."""

    def __init__(
        self,
        calculadora_deducciones: CalculadoraDeducciones | None = None,
        calculadora_beneficios: CalculadoraBeneficios | None = None,
    ) -> None:
        # Inyección de dependencias: facilita el testing con dobles y el
        # reemplazo de estrategias de cálculo (DIP).
        self._deducciones = calculadora_deducciones or CalculadoraDeducciones()
        self._beneficios = calculadora_beneficios or CalculadoraBeneficios()

    def procesar(self, empleado: Empleado) -> ReciboNomina:
        """Genera el recibo de nómina completo de un empleado."""
        salario_bruto = empleado.calcular_salario_bruto()
        deducciones = self._deducciones.calcular(salario_bruto)
        beneficios = self._beneficios.calcular(empleado, salario_bruto)

        recibo = ReciboNomina(
            empleado=empleado,
            salario_bruto=salario_bruto,
            deducciones=deducciones,
            beneficios=beneficios,
        )

        # Regla de negocio: el salario neto nunca puede ser negativo.
        if recibo.salario_neto < 0:
            raise SalarioNetoNegativoError(
                f"El salario neto de {empleado.nombre} resultó negativo: "
                f"{recibo.salario_neto}."
            )
        return recibo
