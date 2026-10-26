"""Utilidades compartidas para las pruebas unitarias."""
from datetime import date
from decimal import Decimal

HOY = date(2026, 10, 20)


def hace_anios(anios: int) -> date:
    """Fecha de ingreso que deja exactamente ``anios`` años de antigüedad."""
    return date(HOY.year - anios, HOY.month, HOY.day)


def decimal(valor: str | int | float) -> Decimal:
    """Convierte de forma segura a ``Decimal`` para las aserciones."""
    return Decimal(str(valor))
