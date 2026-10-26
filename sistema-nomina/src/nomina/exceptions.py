"""Excepciones de dominio del sistema de nómina.

Todas las excepciones propias heredan de :class:`NominaError` para que el
llamador pueda capturar cualquier error de negocio con un único ``except``.
"""


class NominaError(Exception):
    """Excepción base del dominio de nómina."""


class HorasNegativasError(NominaError, ValueError):
    """Se intentó registrar horas trabajadas negativas."""


class VentasNegativasError(NominaError, ValueError):
    """Se intentó registrar ventas negativas."""


class SalarioNetoNegativoError(NominaError):
    """El resultado del cálculo produjo un salario neto negativo."""


class DatosEmpleadosInvalidosError(NominaError, ValueError):
    """Datos de identificación o fechas del empleado inválidos."""
