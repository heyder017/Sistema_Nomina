"""Sistema de nómina: paquete principal."""
from nomina.config import PARAMETROS_POR_DEFECTO, ParametrosNomina
from nomina.exceptions import (
    DatosEmpleadosInvalidosError,
    HorasNegativasError,
    NominaError,
    SalarioNetoNegativoError,
    VentasNegativasError,
)
from nomina.models import Asalariado, Empleado, PorComision, PorHoras, Temporal
from nomina.services import (
    CalculadoraBeneficios,
    CalculadoraDeducciones,
    ProcesadorNomina,
    ReciboNomina,
)

__all__ = [
    "Asalariado",
    "CalculadoraBeneficios",
    "CalculadoraDeducciones",
    "DatosEmpleadosInvalidosError",
    "Empleado",
    "HorasNegativasError",
    "NominaError",
    "PARAMETROS_POR_DEFECTO",
    "ParametrosNomina",
    "PorComision",
    "PorHoras",
    "ProcesadorNomina",
    "ReciboNomina",
    "SalarioNetoNegativoError",
    "Temporal",
    "VentasNegativasError",
]
