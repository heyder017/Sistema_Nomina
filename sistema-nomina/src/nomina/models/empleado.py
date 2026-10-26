"""Modelo base de empleado (abstracción del dominio).

Define el contrato común a todos los tipos de empleado. El cálculo del
salario bruto se deja en ``abstractmethod`` para que cada subclase implemente
su propia forma de calcularlo (Polimorfismo -> OCP: agregar un nuevo tipo de
empleado no exige modificar el código existente).
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal


def calcular_anios_antiguedad(fecha_ingreso: date, fecha_referencia: date | None = None) -> Decimal:
    """Devuelve la antigüedad en años completos (con un decimal de precisión).

    Se usa ``Decimal`` para poder comparar umbrales como ``> 5 años`` de forma
    exacta sin errores de punto flotante.
    """
    referencia = fecha_referencia or date.today()
    dias = (referencia - fecha_ingreso).days
    return Decimal(dias) / Decimal("365.25")


@dataclass(frozen=True)
class Empleado(ABC):
    """Clase base de todos los empleados de la empresa.

    Atributos comunes:
        nombre: Nombre completo del empleado.
        identificacion: Número de documento único (cédula/NIT).
        fecha_ingreso: Fecha de ingreso a la empresa (origen de la antigüedad).
    """

    nombre: str
    identificacion: str
    fecha_ingreso: date

    def __post_init__(self) -> None:
        """Validación de invariantes comunes a todos los empleados."""
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del empleado no puede estar vacío.")
        if not self.identificacion or not self.identificacion.strip():
            raise ValueError("La identificación del empleado no puede estar vacía.")

    # --- Antigüedad -------------------------------------------------------

    def anios_antiguedad(self, fecha_referencia: date | None = None) -> Decimal:
        """Antigüedad del empleado en años, medida en una fecha dada."""
        return calcular_anios_antiguedad(self.fecha_ingreso, fecha_referencia)

    def tiene_mas_anios_que(self, anios: int, fecha_referencia: date | None = None) -> bool:
        """Indica si el empleado supera los ``anios`` completos de servicio."""
        return self.anios_antiguedad(fecha_referencia) > Decimal(anios)

    # --- Contrato ----------------------------------------------------------

    @property
    def es_permanente(self) -> bool:
        """Solo los empleados permanentes reciben beneficios de alimentación."""
        return False

    def accede_fondo_ahorro(self, fecha_referencia: date | None = None) -> bool:
        """Solo los empleados por horas elegibles acceden al fondo de ahorro.

        Se define aquí (y no con ``isinstance`` en el servicio) para respetar
        el Principio de Abierto/Cerrado: añadir un nuevo tipo de empleado no
        obliga a modificar la calculadora de beneficios.
        """
        return False

    # --- Cálculo de salario -------------------------------------------------

    @abstractmethod
    def calcular_salario_bruto(self) -> Decimal:
        """Calcula el salario bruto del periodo según la naturaleza del empleado."""
        raise NotImplementedError
