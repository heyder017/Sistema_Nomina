"""Modelos de dominio del sistema de nómina."""
from nomina.models.asalariado import Asalariado
from nomina.models.empleado import Empleado, calcular_anios_antiguedad
from nomina.models.por_comision import PorComision
from nomina.models.por_horas import PorHoras
from nomina.models.temporal import Temporal

__all__ = [
    "Asalariado",
    "Empleado",
    "PorComision",
    "PorHoras",
    "Temporal",
    "calcular_anios_antiguedad",
]
